import uuid
from datetime import datetime

from schema import AxisMapping, CrossMapping, Confidence
from axes import ALL_SECTIONS, HOW_JOURNEY_AXES, HOW_MECHANISM_AXES


class Session:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().isoformat()
        self.mappings: dict[str, AxisMapping] = {}
        self.cross_mappings: dict[str, CrossMapping] = {}
        self.conversation: list[dict] = []

    def update_mappings(self, new_mappings: list[AxisMapping]):
        for m in new_mappings:
            key = f"{m.section}.{m.axis}"
            self.mappings[key] = m

    def update_cross(self, new_cross: list[CrossMapping]):
        for c in new_cross:
            key = f"{c.journey_axis}:{c.mechanism_axis}"
            self.cross_mappings[key] = c

    def get_completion(self) -> dict[str, float]:
        result = {}
        for section_key, section in ALL_SECTIONS.items():
            total = len(section["axes"])
            filled = sum(
                1 for ax in section["axes"]
                if f"{section_key}.{ax['id']}" in self.mappings
                and self.mappings[f"{section_key}.{ax['id']}"].confidence != Confidence.unknown
            )
            result[section_key] = round(filled / total, 2) if total > 0 else 0.0

        # Cross matrix
        total_cross = len(HOW_JOURNEY_AXES) * len(HOW_MECHANISM_AXES)
        filled_cross = sum(
            1 for c in self.cross_mappings.values()
            if c.confidence != Confidence.unknown
        )
        result["howCross"] = round(filled_cross / total_cross, 2) if total_cross > 0 else 0.0
        return result

    def is_complete(self) -> bool:
        completion = self.get_completion()
        # Exclude howCross from overall check (it's supplementary)
        main_sections = ["who", "what", "howJourney", "howMechanism"]
        total_axes = sum(len(ALL_SECTIONS[s]["axes"]) for s in main_sections)
        filled = sum(
            1 for s in main_sections
            for ax in ALL_SECTIONS[s]["axes"]
            if f"{s}.{ax['id']}" in self.mappings
            and self.mappings[f"{s}.{ax['id']}"].confidence != Confidence.unknown
        )
        return (filled / total_axes) >= 0.8 if total_axes > 0 else False

    def get_state_summary(self) -> str:
        lines = []
        for section_key, section in ALL_SECTIONS.items():
            section_mappings = []
            for ax in section["axes"]:
                key = f"{section_key}.{ax['id']}"
                if key in self.mappings:
                    m = self.mappings[key]
                    section_mappings.append(
                        f"  {ax['id']}({ax['label']}): {m.value} [{m.confidence.value}] - {m.reason}"
                    )
                else:
                    section_mappings.append(f"  {ax['id']}({ax['label']}): unknown")

            completion = self.get_completion()
            lines.append(f"\n{section['label']} (完了度: {completion.get(section_key, 0):.0%})")
            lines.extend(section_mappings)

        if self.cross_mappings:
            lines.append(f"\nクロスマトリクス ({len(self.cross_mappings)}件設定済み)")
            for key, c in self.cross_mappings.items():
                lines.append(f"  {key}: level={c.level} [{c.confidence.value}]")

        return "\n".join(lines)

    def to_stratmap_json(self) -> dict:
        """Export in stratmap-compatible format."""
        result = {
            "version": 1,
            "updatedAt": datetime.now().isoformat(),
        }

        # Who
        who_values = {}
        who_active = []
        for ax in ALL_SECTIONS["who"]["axes"]:
            key = f"who.{ax['id']}"
            if key in self.mappings and self.mappings[key].confidence != Confidence.unknown:
                who_values[ax["id"]] = self.mappings[key].value
                who_active.append(ax["id"])
            else:
                who_values[ax["id"]] = 5
        result["who"] = {"values": who_values, "activeAxes": who_active}

        # What
        what_values = {}
        what_active = []
        for ax in ALL_SECTIONS["what"]["axes"]:
            key = f"what.{ax['id']}"
            if key in self.mappings and self.mappings[key].confidence != Confidence.unknown:
                what_values[ax["id"]] = self.mappings[key].value
                what_active.append(ax["id"])
            else:
                what_values[ax["id"]] = 5
        result["what"] = {"values": what_values, "activeAxes": what_active}

        # How Journey
        hj_values = {}
        for ax in ALL_SECTIONS["howJourney"]["axes"]:
            key = f"howJourney.{ax['id']}"
            if key in self.mappings and self.mappings[key].confidence != Confidence.unknown:
                hj_values[ax["id"]] = self.mappings[key].value
            else:
                hj_values[ax["id"]] = 5
        result["howJourney"] = {"values": hj_values}

        # How Mechanism
        hm_values = {}
        for ax in ALL_SECTIONS["howMechanism"]["axes"]:
            key = f"howMechanism.{ax['id']}"
            if key in self.mappings and self.mappings[key].confidence != Confidence.unknown:
                hm_values[ax["id"]] = self.mappings[key].value
            else:
                hm_values[ax["id"]] = 5
        result["howMechanism"] = {"values": hm_values}

        # How Cross
        j_values = {}
        for ax in HOW_JOURNEY_AXES:
            key = f"howJourney.{ax['id']}"
            j_values[ax["id"]] = self.mappings[key].value if key in self.mappings else 5
        m_values = {}
        for ax in HOW_MECHANISM_AXES:
            key = f"howMechanism.{ax['id']}"
            m_values[ax["id"]] = self.mappings[key].value if key in self.mappings else 5
        relevance = {}
        for j in HOW_JOURNEY_AXES:
            for m in HOW_MECHANISM_AXES:
                cross_key = f"{j['id']}:{m['id']}"
                if cross_key in self.cross_mappings:
                    relevance[cross_key] = self.cross_mappings[cross_key].level
                else:
                    relevance[cross_key] = 0
        result["howCross"] = {
            "jValues": j_values,
            "mValues": m_values,
            "relevance": relevance,
        }

        return result


# In-memory session store
sessions: dict[str, Session] = {}


def create_session() -> Session:
    s = Session()
    sessions[s.id] = s
    return s


def get_session(session_id: str) -> Session | None:
    return sessions.get(session_id)
