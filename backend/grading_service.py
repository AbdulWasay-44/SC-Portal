import json
import re
from typing import Any, Dict, Optional

import requests
import streamlit as st

from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    OPENROUTER_BASE_URL,
    OPENROUTER_APP_NAME,
    OPENROUTER_SITE_URL,
)


class GradingService:
    """Service for grading assignments using OpenRouter chat completions."""

    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.model = OPENROUTER_MODEL
        self.base_url = f"{OPENROUTER_BASE_URL.rstrip('/')}/chat/completions"
        self.app_name = OPENROUTER_APP_NAME
        self.site_url = OPENROUTER_SITE_URL

        if not self.api_key:
            st.warning("OpenRouter API key not found in environment variables")

    def grade_assignment(
        self,
        text_content: str,
        total_marks: int,
        custom_criteria: Dict[str, int],
        additional_instructions: str,
        detect_multiple_questions: bool = True,
    ) -> Dict[str, Any]:
        """Grade an assignment using OpenRouter."""
        try:
            if not self.api_key:
                return self._create_error_result("OpenRouter API key not configured")

            prepared_text = self._prepare_text_for_grading(text_content)
            prompt = self._create_grading_prompt(
                prepared_text,
                total_marks,
                custom_criteria,
                additional_instructions,
                detect_multiple_questions,
            )

            response = self._call_openrouter_api(prompt)
            if not response:
                return self._create_error_result("Failed to get response from OpenRouter")

            return self._parse_grading_response(response, total_marks)

        except Exception as e:
            st.error(f"Error during grading: {str(e)}")
            return self._create_error_result(str(e))

    def _prepare_text_for_grading(self, text_content: str, max_chars: int = 12000) -> str:
        """Trim oversized extracted text to keep routed models responsive."""
        cleaned = text_content.strip()
        if len(cleaned) <= max_chars:
            return cleaned

        head = cleaned[: max_chars // 2]
        tail = cleaned[-max_chars // 2 :]
        return (
            head
            + "\n\n[Content truncated for length. Middle section omitted to fit model limits.]\n\n"
            + tail
        )

    def _create_grading_prompt(
        self,
        text_content: str,
        total_marks: int,
        custom_criteria: Dict[str, int],
        additional_instructions: str,
        detect_multiple_questions: bool,
    ) -> str:
        """Create a grading prompt that asks for strict JSON output."""
        prompt = f"""You are an expert academic grader. Grade the following submission fairly and strictly.

ASSIGNMENT CONTENT TO GRADE:
{text_content}

GRADING PARAMETERS:
- Total Marks Available: {total_marks}
- Detect Multiple Questions: {detect_multiple_questions}
"""

        if custom_criteria:
            prompt += "\nCUSTOM GRADING CRITERIA:\n"
            for criterion, marks in custom_criteria.items():
                prompt += f"- {criterion}: {marks} marks\n"
            prompt += (
                "\nStrict rule: if a criterion requires content that is missing, award 0 for that criterion.\n"
            )

        if additional_instructions:
            prompt += f"\nADDITIONAL INSTRUCTIONS:\n{additional_instructions}\n"

        prompt += """
Return exactly one valid JSON object with this structure:
{
  "total_score": <number>,
  "percentage": <number>,
  "overall_feedback": "<string>",
  "strengths": ["<string>"],
  "areas_for_improvement": ["<string>"],
  "criteria_scores": {
    "<criterion_name>": <number>
  },
  "criteria_explanations": {
    "<criterion_name>": "<brief reason>"
  },
  "questions": [
    {
      "question_number": <number>,
      "question_text": "<string>",
      "score": <number>,
      "max_score": <number>,
      "feedback": "<string>",
      "attempted": <true_or_false>
    }
  ],
  "grade_justification": "<string>"
}

Rules:
- Output valid JSON only, with no markdown fences.
- total_score must be between 0 and the total marks available.
- If questions are not clearly separable, return an empty questions array.
- Keep overall_feedback under 120 words.
- Return at most 3 strengths and 3 areas_for_improvement.
- Keep each criteria explanation under 20 words.
- Be concise but specific.
"""
        return prompt

    def _call_openrouter_api(self, prompt: str) -> Optional[str]:
        """Call OpenRouter with reasoning disabled for more reliable final output."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.app_name,
        }

        primary_payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert academic grader. Respond with exactly one valid JSON object.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
            "max_tokens": 1400,
            "reasoning": {"effort": "none", "exclude": True},
            "stream": False,
        }

        fallback_payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Respond with valid JSON only."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
            "max_tokens": 1100,
            "stream": False,
        }

        for payload in (primary_payload, fallback_payload):
            response_text = self._send_openrouter_request(headers, payload)
            if response_text:
                return response_text

        return None

    def _send_openrouter_request(self, headers: Dict[str, str], payload: Dict[str, Any]) -> Optional[str]:
        """Send a single OpenRouter request and extract assistant content safely."""
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=45)
            if response.status_code != 200:
                st.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                return None

            response_data = response.json()
            choices = response_data.get("choices", [])
            if not choices:
                return None

            message = choices[0].get("message", {})
            content = message.get("content")

            if content:
                return content

            reasoning = message.get("reasoning")
            if reasoning:
                st.warning("The routed model returned reasoning but no final answer. Retrying with a simpler request.")

            return None

        except requests.exceptions.RequestException as e:
            st.error(f"Network error calling OpenRouter API: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Unexpected error calling OpenRouter API: {str(e)}")
            return None

    def _parse_grading_response(self, response: str, total_marks: int) -> Dict[str, Any]:
        """Parse and normalize the model's grading response."""
        try:
            response = response.strip()
            json_match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
            if json_match:
                json_content = json_match.group(1)
            else:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_content = response[json_start:json_end] if json_start != -1 and json_end > json_start else response

            grading_data = json.loads(json_content)

            total_score = self._coerce_number(grading_data.get("total_score", 0))
            total_score = max(0, min(total_score, total_marks))

            percentage = self._coerce_number(grading_data.get("percentage", 0))
            if total_marks > 0:
                percentage = (total_score / total_marks) * 100

            return {
                "total_score": total_score,
                "percentage": percentage,
                "feedback": self._combine_feedback(grading_data),
                "criteria_scores": grading_data.get("criteria_scores", {}) or {},
                "criteria_explanations": grading_data.get("criteria_explanations", {}) or {},
                "questions": self._normalize_questions(grading_data.get("questions", []), total_marks),
                "strengths": grading_data.get("strengths", []) or [],
                "areas_for_improvement": grading_data.get("areas_for_improvement", []) or [],
                "grade_justification": grading_data.get("grade_justification", "") or "",
            }

        except json.JSONDecodeError as e:
            st.error(f"Error parsing AI response as JSON: {str(e)}")
            return self._fallback_text_parsing(response, total_marks)
        except Exception as e:
            st.error(f"Error processing grading response: {str(e)}")
            return self._create_error_result(str(e))

    def _normalize_questions(self, questions: Any, total_marks: int) -> list[Dict[str, Any]]:
        """Normalize question records for analytics/UI usage."""
        if not isinstance(questions, list):
            return []

        normalized = []
        for index, question in enumerate(questions, start=1):
            if not isinstance(question, dict):
                continue

            max_score = self._coerce_number(question.get("max_score", 0))
            score = self._coerce_number(question.get("score", 0))
            if max_score < 0:
                max_score = 0
            if score < 0:
                score = 0
            if max_score > 0:
                score = min(score, max_score)
            else:
                score = min(score, total_marks)

            attempted = question.get("attempted")
            if attempted is None:
                attempted = score > 0 or bool(str(question.get("feedback", "")).strip()) or bool(
                    str(question.get("question_text", "")).strip()
                )

            normalized.append(
                {
                    "question_number": question.get("question_number", index),
                    "question_text": question.get("question_text", ""),
                    "score": score,
                    "max_score": max_score,
                    "feedback": question.get("feedback", ""),
                    "attempted": bool(attempted),
                }
            )

        return normalized

    def _combine_feedback(self, grading_data: Dict[str, Any]) -> str:
        """Combine feedback parts into a single displayable string."""
        feedback_parts = []

        if grading_data.get("overall_feedback"):
            feedback_parts.append(grading_data["overall_feedback"])

        strengths = grading_data.get("strengths") or []
        if strengths:
            feedback_parts.append("Strengths:\n" + "\n".join(f"- {strength}" for strength in strengths))

        improvement_areas = grading_data.get("areas_for_improvement") or []
        if improvement_areas:
            feedback_parts.append(
                "Areas for Improvement:\n" + "\n".join(f"- {area}" for area in improvement_areas)
            )

        if grading_data.get("grade_justification"):
            feedback_parts.append("Grade Justification:\n" + grading_data["grade_justification"])

        return "\n\n".join(feedback_parts)

    def _fallback_text_parsing(self, response: str, total_marks: int) -> Dict[str, Any]:
        """Best-effort extraction if the model returns plain text instead of JSON."""
        score_match = re.search(r"(?:score|marks?)[:\s]*(\d+(?:\.\d+)?)(?:\s*/\s*(\d+(?:\.\d+)?))?", response, re.IGNORECASE)
        score = 0.0
        if score_match:
            score = float(score_match.group(1))
            max_score = float(score_match.group(2)) if score_match.group(2) else float(total_marks)
            if max_score > 0 and max_score != total_marks:
                score = (score / max_score) * total_marks

        score = max(0, min(score, total_marks))
        return {
            "total_score": score,
            "percentage": (score / total_marks) * 100 if total_marks > 0 else 0,
            "feedback": response,
            "criteria_scores": {},
            "criteria_explanations": {},
            "questions": [],
            "strengths": [],
            "areas_for_improvement": [],
            "grade_justification": "Parsed from non-JSON model output.",
        }

    def _create_error_result(self, error_message: str) -> Dict[str, Any]:
        """Create a consistent error response shape."""
        return {
            "total_score": 0,
            "percentage": 0,
            "feedback": f"Error during grading: {error_message}",
            "criteria_scores": {},
            "criteria_explanations": {},
            "questions": [],
            "strengths": [],
            "areas_for_improvement": [],
            "grade_justification": "Grading failed due to technical error.",
        }

    def _coerce_number(self, value: Any) -> float:
        """Convert model-provided numbers or numeric strings into floats."""
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            match = re.search(r"-?\d+(?:\.\d+)?", value)
            if match:
                return float(match.group(0))
        return 0.0

    def validate_api_connection(self) -> bool:
        """Test whether OpenRouter is reachable with the current key."""
        if not self.api_key:
            return False

        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": self.site_url,
                "X-Title": self.app_name,
            }
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "Reply with ok"}],
                "max_tokens": 10,
                "reasoning": {"effort": "none", "exclude": True},
                "stream": False,
            }
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=15)
            return response.status_code == 200
        except Exception:
            return False

    def generate_student_feedback(
        self,
        text_content: str,
        subject: str,
        submission_type: str,
    ) -> Dict[str, Any]:
        """Generate student-facing feedback and recommendations."""
        prompt = f"""You are an academic support assistant.

Analyze this student {submission_type.lower()} for the subject "{subject}" and return exactly one valid JSON object.

STUDENT SUBMISSION:
{self._prepare_text_for_grading(text_content, max_chars=9000)}

Return this JSON structure only:
{{
  "estimated_score": <number between 0 and 100>,
  "mistake_identification": ["<short point>"],
  "grammar_spelling_suggestions": ["<short point>"],
  "conceptual_feedback": ["<short point>"],
  "improvement_recommendations": ["<short point>"],
  "suggested_learning_resources": ["<short point>"],
  "weak_areas": ["<short point>"],
  "strong_areas": ["<short point>"]
}}

Rules:
- Keep each list to at most 3 items.
- Be direct, practical, and student-friendly.
- If the submission is too short, say that clearly in mistake_identification.
"""
        response = self._call_openrouter_api(prompt)
        if not response:
            return self._fallback_student_feedback(text_content, subject)

        try:
            parsed = self._extract_json(response)
            data = json.loads(parsed)
            return {
                "estimated_score": max(0, min(self._coerce_number(data.get("estimated_score", 0)), 100)),
                "mistake_identification": data.get("mistake_identification", []) or [],
                "grammar_spelling_suggestions": data.get("grammar_spelling_suggestions", []) or [],
                "conceptual_feedback": data.get("conceptual_feedback", []) or [],
                "improvement_recommendations": data.get("improvement_recommendations", []) or [],
                "suggested_learning_resources": data.get("suggested_learning_resources", []) or [],
                "weak_areas": data.get("weak_areas", []) or [],
                "strong_areas": data.get("strong_areas", []) or [],
            }
        except Exception:
            return self._fallback_student_feedback(text_content, subject)

    def _extract_json(self, response: str) -> str:
        """Extract a JSON object from model output."""
        response = response.strip()
        json_match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
        if json_match:
            return json_match.group(1)
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        if json_start != -1 and json_end > json_start:
            return response[json_start:json_end]
        return response

    def _fallback_student_feedback(self, text_content: str, subject: str) -> Dict[str, Any]:
        """Fallback student support response if the model fails."""
        word_count = len(text_content.split())
        estimated_score = 75 if word_count > 250 else 62 if word_count > 120 else 48
        return {
            "estimated_score": estimated_score,
            "mistake_identification": [
                "Some answers may be too brief for full marks." if word_count < 150 else "A few explanations could be more detailed."
            ],
            "grammar_spelling_suggestions": [
                "Review sentence clarity, punctuation, and spelling before final submission."
            ],
            "conceptual_feedback": [
                f"Strengthen core {subject} concepts with more precise definitions and examples."
            ],
            "improvement_recommendations": [
                "Add clearer explanations, examples, and stronger conclusion points."
            ],
            "suggested_learning_resources": [
                f"Revise lecture notes, textbook summaries, and practice questions for {subject}."
            ],
            "weak_areas": ["Depth of explanation"],
            "strong_areas": ["Basic topic coverage"] if word_count > 100 else [],
        }
