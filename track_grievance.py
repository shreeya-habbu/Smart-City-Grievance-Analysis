import customtkinter as ctk

from database import get_grievance


# ============================================================
# COSMIC THEME
# ============================================================

BG = "#080B1A"
CARD = "#11172B"
CARD_HOVER = "#18213D"

PRIMARY = "#7C4DFF"
PRIMARY_HOVER = "#936BFF"
AI_CYAN = "#4DD9FF"

TEXT = "#F4F2FF"
MUTED = "#9299B5"
BORDER = "#202A48"
BORDER_HOVER = "#5940A8"

GREEN = "#55D6A5"
ORANGE = "#FFB84D"
RED = "#FF647C"
BLUE = "#5EAFFF"


# ============================================================
# TRACK GRIEVANCE PAGE
# ============================================================

class TrackGrievancePage(ctk.CTkFrame):

    def __init__(self, parent, on_back=None):

        super().__init__(
            parent,
            fg_color=BG
        )

        self.on_back = on_back

        self.create_page()


    # ========================================================
    # MAIN PAGE
    # ========================================================

    def create_page(self):

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_frame.pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text="Track Grievance",
            font=("Arial", 27, "bold"),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Check the current status and details of your complaint",
            font=("Arial", 12),
            text_color=MUTED
        ).pack(
            anchor="w",
            pady=(4, 0)
        )


        # ----------------------------------------------------
        # SEARCH CARD
        # ----------------------------------------------------

        search_card = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )

        search_card.pack(
            fill="x",
            padx=30,
            pady=(0, 18)
        )

        ctk.CTkLabel(
            search_card,
            text="Enter Grievance ID",
            font=("Arial", 12, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 6)
        )


        search_row = ctk.CTkFrame(
            search_card,
            fg_color="transparent"
        )

        search_row.pack(
            fill="x",
            padx=18,
            pady=(0, 16)
        )


        self.id_entry = ctk.CTkEntry(
            search_row,
            height=42,
            width=380,
            corner_radius=10,
            fg_color="#0C1122",
            border_color=BORDER,
            text_color=TEXT,
            placeholder_text="Example: GRV-0001",
            placeholder_text_color=MUTED
        )

        self.id_entry.pack(
            side="left"
        )

        self.id_entry.bind(
            "<Return>",
            lambda event: self.track_grievance()
        )


        self.track_button = ctk.CTkButton(
            search_row,
            text="🔍  Track Grievance",
            width=155,
            height=42,
            corner_radius=10,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=("Arial", 11, "bold"),
            command=self.track_grievance
        )

        self.track_button.pack(
            side="left",
            padx=(10, 0)
        )


        # ----------------------------------------------------
        # RESULT AREA
        # ----------------------------------------------------

        self.result_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#252E4B",
            scrollbar_button_hover_color=PRIMARY
        )

        self.result_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )


        self.show_initial_state()


    # ========================================================
    # INITIAL STATE
    # ========================================================

    def show_initial_state(self):

        for widget in self.result_frame.winfo_children():
            widget.destroy()

        card = ctk.CTkFrame(
            self.result_frame,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="x",
            pady=10
        )

        ctk.CTkLabel(
            card,
            text="⌁",
            font=("Arial", 38),
            text_color=PRIMARY
        ).pack(
            pady=(30, 5)
        )

        ctk.CTkLabel(
            card,
            text="Enter a grievance ID to begin",
            font=("Arial", 17, "bold"),
            text_color=TEXT
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            card,
            text="Use the ID received after submitting your grievance.",
            font=("Arial", 11),
            text_color=MUTED
        ).pack(
            pady=(0, 30)
        )


    # ========================================================
    # TRACK GRIEVANCE
    # ========================================================

    def track_grievance(self):

        grievance_id = self.id_entry.get().strip()

        if not grievance_id:

            self.show_message(
                "Please enter a grievance ID.",
                "Enter Grievance ID"
            )

            return


        # Remove GRV- prefix

        clean_id = grievance_id.upper().replace(
            "GRV-",
            ""
        ).strip()


        try:

            grievance_id_number = int(clean_id)

        except ValueError:

            self.show_message(
                "Invalid grievance ID.\n\nExample: GRV-0001",
                "Invalid ID"
            )

            return


        self.track_button.configure(
            text="Searching...",
            state="disabled"
        )

        self.result_frame.after(
            100,
            lambda: self._load_grievance(
                grievance_id_number
            )
        )


    # ========================================================
    # LOAD GRIEVANCE
    # ========================================================

    def _load_grievance(self, grievance_id):

        grievance = get_grievance(
            grievance_id
        )

        self.track_button.configure(
            text="🔍  Track Grievance",
            state="normal"
        )

        if not grievance:

            self.show_not_found()

            return

        self.display_grievance(
            grievance
        )


    # ========================================================
    # DISPLAY GRIEVANCE
    # ========================================================

    def display_grievance(self, grievance):

        for widget in self.result_frame.winfo_children():
            widget.destroy()


        grievance_id = grievance["id"]

        title = grievance["title"] or "Untitled"

        description = (
            grievance["description"]
            or "No description available."
        )

        category = (
            grievance["category"]
            or "Unknown"
        )

        priority = (
            grievance["priority"]
            or "Low"
        )

        severity = (
            grievance["severity"]
            or "Medium"
        )

        status = (
            grievance["status"]
            or "Pending"
        )

        location = (
            grievance["location"]
            or "Not specified"
        )

        created_at = (
            grievance["created_at"]
            or "Unknown"
        )

        ai_summary = (
            grievance["ai_summary"]
            or "No AI summary available."
        )


        # ----------------------------------------------------
        # MAIN RESULT CARD
        # ----------------------------------------------------

        card = ctk.CTkFrame(
            self.result_frame,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="x",
            pady=8
        )


        # ----------------------------------------------------
        # TOP HEADER
        # ----------------------------------------------------

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=20,
            pady=(18, 8)
        )


        ctk.CTkLabel(
            top,
            text=f"GRV-{grievance_id:04d}",
            font=("Arial", 13, "bold"),
            text_color=AI_CYAN
        ).pack(
            side="left"
        )


        self.create_status_badge(
            top,
            status,
            self.get_status_color(status)
        )


        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 21, "bold"),
            text_color=TEXT,
            anchor="w"
        ).pack(
            fill="x",
            padx=20,
            pady=(4, 15)
        )


        # ----------------------------------------------------
        # STATUS SECTION
        # ----------------------------------------------------

        status_card = ctk.CTkFrame(
            card,
            fg_color="#0C1122",
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        status_card.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        ctk.CTkLabel(
            status_card,
            text="CURRENT STATUS",
            font=("Arial", 9, "bold"),
            text_color=MUTED
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 2)
        )


        ctk.CTkLabel(
            status_card,
            text=status,
            font=("Arial", 18, "bold"),
            text_color=self.get_status_color(status)
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )


        # ----------------------------------------------------
        # INFORMATION GRID
        # ----------------------------------------------------

        info = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        info.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )


        self.create_info_item(
            info,
            "Category",
            category
        )

        self.create_info_item(
            info,
            "Priority",
            priority
        )

        self.create_info_item(
            info,
            "Severity",
            severity
        )

        self.create_info_item(
            info,
            "Location",
            location
        )

        self.create_info_item(
            info,
            "Submitted",
            created_at
        )


        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        self.create_section(
            card,
            "Complaint Description",
            description,
            TEXT
        )


        # ----------------------------------------------------
        # AI SUMMARY
        # ----------------------------------------------------

        ai_card = ctk.CTkFrame(
            card,
            fg_color="#0D1930",
            corner_radius=12,
            border_width=1,
            border_color="#27385E"
        )

        ai_card.pack(
            fill="x",
            padx=20,
            pady=(5, 15)
        )


        ctk.CTkLabel(
            ai_card,
            text="✦  AI-Assisted Summary",
            font=("Arial", 12, "bold"),
            text_color=AI_CYAN
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )


        ctk.CTkLabel(
            ai_card,
            text=ai_summary,
            font=("Arial", 11),
            text_color=TEXT,
            justify="left",
            anchor="w",
            wraplength=850
        ).pack(
            fill="x",
            padx=15,
            pady=(0, 12)
        )


        # ----------------------------------------------------
        # RESPONSIBLE AI
        # ----------------------------------------------------

        responsible = ctk.CTkFrame(
            card,
            fg_color="#16152A",
            corner_radius=10,
            border_width=1,
            border_color="#302C55"
        )

        responsible.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )


        ctk.CTkLabel(
            responsible,
            text="⚠  Responsible AI",
            font=("Arial", 10, "bold"),
            text_color=ORANGE
        ).pack(
            anchor="w",
            padx=13,
            pady=(10, 3)
        )


        ctk.CTkLabel(
            responsible,
            text=(
                "AI-generated classification and summary are "
                "recommendations only and should not be treated "
                "as a final administrative decision."
            ),
            font=("Arial", 10),
            text_color=MUTED,
            justify="left",
            anchor="w",
            wraplength=850
        ).pack(
            fill="x",
            padx=13,
            pady=(0, 10)
        )


        # ----------------------------------------------------
        # CARD HOVER
        # ----------------------------------------------------

        self.add_hover_effect(card)


    # ========================================================
    # INFORMATION ITEM
    # ========================================================

    def create_info_item(
        self,
        parent,
        label,
        value
    ):

        item = ctk.CTkFrame(
            parent,
            fg_color="#0C1122",
            corner_radius=10
        )

        item.pack(
            side="left",
            fill="x",
            expand=True,
            padx=4,
            pady=4
        )


        ctk.CTkLabel(
            item,
            text=label.upper(),
            font=("Arial", 8, "bold"),
            text_color=MUTED
        ).pack(
            anchor="w",
            padx=10,
            pady=(9, 1)
        )


        ctk.CTkLabel(
            item,
            text=str(value),
            font=("Arial", 10, "bold"),
            text_color=TEXT,
            anchor="w"
        ).pack(
            anchor="w",
            padx=10,
            pady=(0, 9)
        )


    # ========================================================
    # SECTION
    # ========================================================

    def create_section(
        self,
        parent,
        title,
        text,
        text_color
    ):

        section = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        section.pack(
            fill="x",
            padx=20,
            pady=(0, 12)
        )


        ctk.CTkLabel(
            section,
            text=title,
            font=("Arial", 11, "bold"),
            text_color=SECONDARY,
            anchor="w"
        ).pack(
            anchor="w",
            pady=(0, 4)
        )


        ctk.CTkLabel(
            section,
            text=text,
            font=("Arial", 11),
            text_color=text_color,
            justify="left",
            anchor="w",
            wraplength=850
        ).pack(
            fill="x"
        )


    # ========================================================
    # STATUS BADGE
    # ========================================================

    def create_status_badge(
        self,
        parent,
        text,
        color
    ):

        ctk.CTkLabel(
            parent,
            text=text,
            font=("Arial", 10, "bold"),
            text_color=color,
            fg_color="#0C1122",
            corner_radius=8,
            padx=10,
            pady=5
        ).pack(
            side="right"
        )


    # ========================================================
    # NOT FOUND
    # ========================================================

    def show_not_found(self):

        for widget in self.result_frame.winfo_children():
            widget.destroy()


        card = ctk.CTkFrame(
            self.result_frame,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color="#39243A"
        )

        card.pack(
            fill="x",
            pady=10
        )


        ctk.CTkLabel(
            card,
            text="?",
            font=("Arial", 38, "bold"),
            text_color=RED
        ).pack(
            pady=(30, 5)
        )


        ctk.CTkLabel(
            card,
            text="Grievance Not Found",
            font=("Arial", 17, "bold"),
            text_color=TEXT
        ).pack(pady=(0, 5))


        ctk.CTkLabel(
            card,
            text="Please check the grievance ID and try again.",
            font=("Arial", 11),
            text_color=MUTED
        ).pack(
            pady=(0, 30)
        )


    # ========================================================
    # MESSAGE
    # ========================================================

    def show_message(
        self,
        message,
        title="Information"
    ):

        dialog = ctk.CTkToplevel(self)

        dialog.title(title)
        dialog.geometry("400x220")
        dialog.resizable(False, False)

        dialog.configure(
            fg_color=BG
        )

        dialog.transient(
            self.winfo_toplevel()
        )

        dialog.grab_set()


        ctk.CTkLabel(
            dialog,
            text=title,
            font=("Arial", 18, "bold"),
            text_color=TEXT
        ).pack(
            pady=(30, 10)
        )


        ctk.CTkLabel(
            dialog,
            text=message,
            font=("Arial", 11),
            text_color=MUTED,
            justify="center"
        ).pack(
            padx=25,
            pady=5
        )


        ctk.CTkButton(
            dialog,
            text="OK",
            width=100,
            height=35,
            corner_radius=8,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            command=dialog.destroy
        ).pack(
            pady=20
        )


    # ========================================================
    # HOVER EFFECT
    # ========================================================

    def add_hover_effect(self, card):

        def enter(event):

            if card.winfo_exists():

                card.configure(
                    fg_color=CARD_HOVER,
                    border_color=BORDER_HOVER
                )


        def leave(event):

            if card.winfo_exists():

                card.configure(
                    fg_color=CARD,
                    border_color=BORDER
                )


        card.bind(
            "<Enter>",
            enter,
            add="+"
        )

        card.bind(
            "<Leave>",
            leave,
            add="+"
        )


    # ========================================================
    # STATUS COLOR
    # ========================================================

    def get_status_color(
        self,
        status
    ):

        colors = {
            "Pending": ORANGE,
            "In Progress": BLUE,
            "Resolved": GREEN
        }

        return colors.get(
            status,
            MUTED
        )