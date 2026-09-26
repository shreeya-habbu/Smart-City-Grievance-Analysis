import customtkinter as ctk
from tkinter import messagebox

from database import add_grievance
from ai_analysis import analyze_grievance
from llm_service import analyze_with_gemini


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#FFF6E9"
PRIMARY = "#6750A4"
SECONDARY = "#A78BFA"
ACCENT = "#7EC8E3"
SUCCESS = "#8FD8B8"
GOLD = "#FDD88A"
CARD = "#F4F0FF"
TEXT = "#2E2E2E"
MUTED = "#777777"


# ============================================================
# GEMINI RESPONSE PARSER
# ============================================================

def parse_gemini_response(response):
    """
    Convert Gemini's text response into the dictionary format
    already used by the database and dashboard.
    """

    result = {
        "category": "",
        "priority": "",
        "severity": "",
        "summary": "",
        "reason": ""
    }

    if not response:
        return None

    lines = response.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Remove markdown formatting such as **Category:**
        clean_line = line.replace("**", "").strip()

        if ":" not in clean_line:
            continue

        key, value = clean_line.split(":", 1)

        key = key.strip().lower()
        value = value.strip()

        if key == "category":
            result["category"] = value

        elif key == "priority":
            result["priority"] = value

        elif key == "severity":
            result["severity"] = value

        elif key == "summary":
            result["summary"] = value

        elif key == "reason":
            result["reason"] = value

    # Make sure all important fields were received
    required_fields = [
        "category",
        "priority",
        "severity",
        "summary",
        "reason"
    ]

    for field in required_fields:
        if not result[field]:
            return None

    return result


# ============================================================
# CITIZEN GRIEVANCE PAGE
# ============================================================

class GrievancePage(ctk.CTkFrame):

    def __init__(self, parent, on_back=None):

        super().__init__(
            parent,
            fg_color=BG_COLOR
        )

        self.on_back = on_back

        self.create_header()
        self.create_form()

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color=PRIMARY,
            corner_radius=0,
            height=75
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        back_button = ctk.CTkButton(
            header,
            text="← Back",
            width=90,
            height=38,
            fg_color="transparent",
            hover_color=SECONDARY,
            command=self.go_back
        )

        back_button.pack(
            side="left",
            padx=20
        )

        title = ctk.CTkLabel(
            header,
            text="Submit a Civic Grievance",
            font=("Arial", 24, "bold"),
            text_color="white"
        )

        title.pack(
            side="left",
            padx=10
        )

    # --------------------------------------------------------
    # FORM
    # --------------------------------------------------------

    def create_form(self):

        container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=50,
            pady=30
        )

        # -----------------------------
        # Intro
        # -----------------------------

        ctk.CTkLabel(
            container,
            text="Tell us about the problem",
            font=("Arial", 28, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            container,
            text=(
                "Provide accurate details so the city administration "
                "can understand and respond to your grievance."
            ),
            font=("Arial", 14),
            text_color=MUTED
        ).pack(
            anchor="w",
            pady=(5, 25)
        )

        # -----------------------------
        # Citizen Information
        # -----------------------------

        info_card = ctk.CTkFrame(
            container,
            fg_color=CARD,
            corner_radius=18
        )

        info_card.pack(
            fill="x",
            pady=10
        )

        ctk.CTkLabel(
            info_card,
            text="Citizen Information",
            font=("Arial", 18, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        self.name_entry = self.create_entry(
            info_card,
            "Full Name"
        )

        self.contact_entry = self.create_entry(
            info_card,
            "Contact Number / Email"
        )

        # -----------------------------
        # Grievance Information
        # -----------------------------

        grievance_card = ctk.CTkFrame(
            container,
            fg_color=CARD,
            corner_radius=18
        )

        grievance_card.pack(
            fill="x",
            pady=10
        )

        ctk.CTkLabel(
            grievance_card,
            text="Grievance Details",
            font=("Arial", 18, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        self.title_entry = self.create_entry(
            grievance_card,
            "Grievance Title"
        )

        self.location_entry = self.create_entry(
            grievance_card,
            "Location / Area"
        )

        ctk.CTkLabel(
            grievance_card,
            text="Describe the issue",
            font=("Arial", 14, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=25,
            pady=(15, 5)
        )

        self.description_box = ctk.CTkTextbox(
            grievance_card,
            height=150,
            corner_radius=12,
            fg_color="white",
            text_color=TEXT,
            border_width=1,
            border_color="#DDD5F2"
        )

        self.description_box.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        # -----------------------------
        # AI Information
        # -----------------------------

        ai_info = ctk.CTkFrame(
            container,
            fg_color="#EEE8FF",
            corner_radius=15
        )

        ai_info.pack(
            fill="x",
            pady=15
        )

        ctk.CTkLabel(
            ai_info,
            text="✦ AI-Powered Analysis",
            font=("Arial", 17, "bold"),
            text_color=PRIMARY
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            ai_info,
            text=(
                "After submission, Gemini AI will analyze the grievance "
                "and estimate its category, priority and severity."
            ),
            font=("Arial", 13),
            text_color=TEXT,
            wraplength=850,
            justify="left"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # -----------------------------
        # Privacy & Responsible AI
        # -----------------------------

        privacy_info = ctk.CTkFrame(
            container,
            fg_color="#F4F0FF",
            corner_radius=15
        )

        privacy_info.pack(
            fill="x",
            pady=5
        )

        ctk.CTkLabel(
            privacy_info,
            text="🔒 Privacy & Responsible AI",
            font=("Arial", 16, "bold"),
            text_color=PRIMARY
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            privacy_info,
            text=(
                "Please provide only information necessary to process your grievance. "
                "AI-generated category, priority and severity are recommendations only "
                "and must be reviewed by an authorized administrator."
            ),
            font=("Arial", 12),
            text_color=TEXT,
            wraplength=850,
            justify="left"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # -----------------------------
        # Submit Button
        # -----------------------------

        self.submit_button = ctk.CTkButton(
            container,
            text="Submit Grievance  →",
            height=50,
            width=250,
            corner_radius=12,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            font=("Arial", 16, "bold"),
            command=self.submit_grievance
        )

        self.submit_button.pack(
            pady=25
        )

    # --------------------------------------------------------
    # ENTRY CREATOR
    # --------------------------------------------------------

    def create_entry(self, parent, placeholder):

        entry = ctk.CTkEntry(
            parent,
            height=42,
            corner_radius=10,
            placeholder_text=placeholder,
            fg_color="white",
            text_color=TEXT,
            border_color="#DDD5F2",
            border_width=1
        )

        entry.pack(
            fill="x",
            padx=25,
            pady=7
        )

        return entry

    # --------------------------------------------------------
    # SUBMIT GRIEVANCE
    # --------------------------------------------------------

    def submit_grievance(self):

        name = self.name_entry.get().strip()
        contact = self.contact_entry.get().strip()
        title = self.title_entry.get().strip()
        location = self.location_entry.get().strip()

        description = self.description_box.get(
            "1.0",
            "end"
        ).strip()

        # -----------------------------
        # Validation
        # -----------------------------

        if not name:
            messagebox.showwarning(
                "Missing Information",
                "Please enter your name."
            )
            return

        if not title:
            messagebox.showwarning(
                "Missing Information",
                "Please enter a grievance title."
            )
            return

        if not description:
            messagebox.showwarning(
                "Missing Information",
                "Please describe the issue."
            )
            return

        if not location:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the location."
            )
            return

        # -----------------------------
        # Disable button while AI works
        # -----------------------------

        self.submit_button.configure(
            state="disabled",
            text="AI is analyzing..."
        )

        self.update()

        # -----------------------------
        # GEMINI AI ANALYSIS
        # -----------------------------

        grievance_text = f"""
        Title: {title}

        Location: {location}

        Description: {description}
        """

        gemini_response = analyze_with_gemini(
            grievance_text
        )

        analysis = parse_gemini_response(
            gemini_response
        )

        # -----------------------------
        # FALLBACK AI
        # -----------------------------

        if analysis is None:

            analysis = analyze_grievance(
                title,
                description
            )

            ai_source = "Fallback AI"

        else:

            ai_source = "Gemini AI"

        # -----------------------------
        # DATABASE
        # -----------------------------

        grievance_id = add_grievance(
            citizen_name=name,
            contact=contact,
            title=title,
            description=description,
            location=location,
            category=analysis["category"],
            priority=analysis["priority"],
            severity=analysis["severity"],
            ai_summary=analysis["summary"],
            ai_reason=analysis["reason"]
        )

        # -----------------------------
        # Re-enable button
        # -----------------------------

        self.submit_button.configure(
            state="normal",
            text="Submit Grievance  →"
        )

        # -----------------------------
        # Success Message
        # -----------------------------

        messagebox.showinfo(
            "Grievance Submitted",
            (
                f"Your grievance has been submitted successfully.\n\n"
                f"Grievance ID: GRV-{grievance_id:04d}\n\n"
                f"AI Source: {ai_source}\n"
                f"Category: {analysis['category']}\n"
                f"Priority: {analysis['priority']}\n"
                f"Severity: {analysis['severity']}\n\n"
                "Note: AI classifications are recommendations only "
                "and should be reviewed by an authorized administrator."
            )
        )

        self.clear_form()

    # --------------------------------------------------------
    # CLEAR FORM
    # --------------------------------------------------------

    def clear_form(self):

        self.name_entry.delete(
            0,
            "end"
        )

        self.contact_entry.delete(
            0,
            "end"
        )

        self.title_entry.delete(
            0,
            "end"
        )

        self.location_entry.delete(
            0,
            "end"
        )

        self.description_box.delete(
            "1.0",
            "end"
        )

    # --------------------------------------------------------
    # BACK
    # --------------------------------------------------------

    def go_back(self):

        if self.on_back:
            self.on_back()