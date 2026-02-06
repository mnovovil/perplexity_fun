"""
Session wrapper that holds chat memory and persists it to disk.

This is a lightweight client that reuses a Perplexity client and
keeps a conversation history locally so subsequent queries include
prior messages (chat memory). It persists minimal state to a JSON
file (not credentials).
"""
from __future__ import annotations

import json
import os
from typing import List, Dict, Optional
from datetime import datetime

from perplexity import Perplexity


class QueryClient:
    """Client that holds a persistent chat history and reuses a Perplexity client.

    - Keeps an in-memory `history` list of messages (role/text/timestamp).
    - Persists minimal state to a JSON file (default: ./perplexity_session.json).
    - Rebuilds a prompt containing recent history for each request so the chat "remembers".
    """

    def __init__(
        self,
        preset: Optional[str] = None,
        state_path: Optional[str] = None,
        max_history_items: int = 20,
    ) -> None:
        self.client = Perplexity()
        self.preset = preset or os.getenv("PERPLEXITY_PRESET", "sonar")
        # Default session file in user data directory for persistence across restarts
        default_dir = os.path.join(os.path.expanduser("~"), ".perplexity")
        try:
            os.makedirs(default_dir, exist_ok=True)
        except Exception:
            default_dir = os.getcwd()
        self.state_path = state_path or os.path.join(default_dir, "session.json")
        self.max_history_items = max_history_items
        self.history: List[Dict] = []
        self._load_state()

    def _load_state(self) -> None:
        if os.path.exists(self.state_path):
            try:
                with open(self.state_path, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                    self.history = data.get("history", []) or []
            except Exception:
                # If state is corrupt, start fresh
                self.history = []

    def _save_state(self) -> None:
        data = {"history": self.history}
        with open(self.state_path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

    def _format_history_prompt(self) -> str:
        items = self.history[- self.max_history_items :]
        lines = []
        for item in items:
            role = item.get("role", "user")
            text = item.get("text", "")
            lines.append(f"{role.capitalize()}: {text}")
        return "\n".join(lines)

    def query(self, text: str, persist: bool = True) -> str:
        """Send a query while including recent conversation history.

        Args:
            text: User message to send.
            persist: Whether to persist updated history to disk.

        Returns:
            The assistant's text response.
        """
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Add the user message to history
        self.history.append({"role": "user", "text": text, "ts": timestamp})

        # Build prompt combining recent history
        history_prompt = self._format_history_prompt()
        if history_prompt:
            prompt = f"{history_prompt}\nAssistant:"
            # We append the new user text explicitly so it's clear in the prompt
            prompt = f"{history_prompt}\nUser: {text}\nAssistant:"
        else:
            prompt = f"User: {text}\nAssistant:"

        # Call the Perplexity client (keeps behaviour of existing code)
        response = self.client.responses.create(preset=self.preset, input=prompt)
        output = getattr(response, "output_text", str(response))

        # Store assistant reply
        self.history.append({"role": "assistant", "text": output, "ts": datetime.utcnow().isoformat() + "Z"})

        if persist:
            try:
                self._save_state()
            except Exception:
                # Don't raise on persistence failure; keep in-memory history
                pass

        return output

    def clear_history(self, persist: bool = True) -> None:
        """Clear conversation history."""
        self.history = []
        if persist:
            try:
                self._save_state()
            except Exception:
                pass


__all__ = ["QueryClient"]
