import customtkinter as ctk

from database import (
    get_all_grievances,
    update_status
)


# ============================================================
# COSMIC THEME
# ============================================================

BG = "#080B1A"
CARD = "#11172B"
CARD_HOVER = "#18213D"

PRIMARY = "#7C4DFF"
PRIMARY_HOVER = "#936BFF"
SECONDARY = "#A970FF"
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
# GRIEVANCE MANAGEMENT PAGE
# ============================================================

class GrievanceManagementPage(ctk.CTkFrame):

    def __init__(self, parent, on_back=None):

        super().__init__(
            parent,
            fg_color=BG
        )

        self.on_back = on_back
        self.all_grievances = []

        self.create_page()
        self.load_grievances()


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
            text="Grievance Management",
            font=("Arial", 27, "bold"),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Review, manage and update citizen complaints",
            font=("Arial", 12),
            text_color=MUTED
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        self.refresh_button = ctk.CTkButton(
            header,
            text="⟳  Refresh",
            width=115,
            height=38,
            corner_radius=10,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=("Arial", 11, "bold"),
            command=self.load_grievances
        )

        self.refresh_button.pack(side="right")


        # ----------------------------------------------------
        # FILTER CARD
        # ----------------------------------------------------

        filter_card = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER
        )

        filter_card.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        # Search

        self.search_entry = ctk.CTkEntry(
            filter_card,
            height=40,
            width=330,
            corner_radius=10,
            fg_color="#0C1122",
            border_color=BORDER,
            text_color=TEXT,
            placeholder_text="⌕  Search grievances...",
            placeholder_text_color=MUTED
        )

        self.search_entry.pack(
            side="left",
            padx=15,
            pady=15
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.apply_filters()
        )


        # Status filter

        self.status_filter = ctk.CTkComboBox(
            filter_card,
            values=[
                "All Status",
                "Pending",
                "In Progress",
                "Resolved"
            ],
            width=160,
            height=40,
            corner_radius=10,
            fg_color="#0C1122",
            border_color=BORDER,
            button_color=PRIMARY,
            button_hover_color=PRIMARY_HOVER,
            text_color=TEXT,
            dropdown_fg_color=CARD,
            dropdown_hover_color=CARD_HOVER,
            dropdown_text_color=TEXT,
            command=lambda value: self.apply_filters()
        )

        self.status_filter.set("All Status")

        self.status_filter.pack(
            side="left",
            padx=8,
            pady=15
        )


        # Priority filter

        self.priority_filter = ctk.CTkComboBox(
            filter_card,
            values=[
                "All Priority",
                "Critical",
                "High",
                "Medium",
                "Low"
            ],
            width=160,
            height=40,
            corner_radius=10,
            fg_color="#0C1122",
            border_color=BORDER,
            button_color=PRIMARY,
            button_hover_color=PRIMARY_HOVER,
            text_color=TEXT,
            dropdown_fg_color=CARD,
            dropdown_hover_color=CARD_HOVER,
            dropdown_text_color=TEXT,
            command=lambda value: self.apply_filters()
        )

        self.priority_filter.set("All Priority")

        self.priority_filter.pack(
            side="left",
            padx=8,
            pady=15
        )


        # ----------------------------------------------------
        # SCROLLABLE LIST
        # ----------------------------------------------------

        self.list_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#252E4B",
            scrollbar_button_hover_color=PRIMARY
        )

        self.list_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )


    # ========================================================
    # LOAD DATA
    # ========================================================

    def load_grievances(self):

        self.refresh_button.configure(
            text="Updating...",
            state="disabled"
        )

        self.after(
            100,
            self._finish_loading
        )


    def _finish_loading(self):

        self.all_grievances = get_all_grievances()

        self.apply_filters()

        self.refresh_button.configure(
            text="⟳  Refresh",
            state="normal"
        )


    # ========================================================
    # FILTER
    # ========================================================

    def apply_filters(self):

        search_text = self.search_entry.get().strip().lower()

        status_value = self.status_filter.get()
        priority_value = self.priority_filter.get()

        filtered = []

        for grievance in self.all_grievances:

            grievance_id = grievance["id"]

            title = grievance["title"] or ""
            description = grievance["description"] or ""
            category = grievance["category"] or ""
            location = grievance["location"] or ""

            status = grievance["status"] or "Pending"
            priority = grievance["priority"] or "Low"

            searchable_text = (
                str(grievance_id)
                + " "
                + title
                + " "
                + description
                + " "
                + category
                + " "
                + location
            ).lower()

            if search_text and search_text not in searchable_text:
                continue

            if (
                status_value != "All Status"
                and status != status_value
            ):
                continue

            if (
                priority_value != "All Priority"
                and priority != priority_value
            ):
                continue

            filtered.append(grievance)

        self.display_grievances(filtered)


    # ========================================================
    # DISPLAY GRIEVANCES
    # ========================================================

    def display_grievances(self, grievances):

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not grievances:

            empty_card = ctk.CTkFrame(
                self.list_frame,
                fg_color=CARD,
                corner_radius=15,
                border_width=1,
                border_color=BORDER
            )

            empty_card.pack(
                fill="x",
                pady=10
            )

            ctk.CTkLabel(
                empty_card,
                text="◌",
                font=("Arial", 30),
                text_color=PRIMARY
            ).pack(
                pady=(30, 5)
            )

            ctk.CTkLabel(
                empty_card,
                text="No grievances found",
                font=("Arial", 17, "bold"),
                text_color=TEXT
            ).pack(pady=(0, 5))

            ctk.CTkLabel(
                empty_card,
                text="Try changing your search or filters.",
                font=("Arial", 11),
                text_color=MUTED
            ).pack(
                pady=(0, 30)
            )

            return

        for grievance in grievances:
            self.create_grievance_card(grievance)


    # ========================================================
    # GRIEVANCE CARD
    # ========================================================

    def create_grievance_card(self, grievance):

        card = ctk.CTkFrame(
            self.list_frame,
            fg_color=CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="x",
            pady=7
        )


        # ----------------------------------------------------
        # TOP ROW
        # ----------------------------------------------------

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=18,
            pady=(15, 5)
        )

        grievance_id = grievance["id"]

        title = grievance["title"] or "Untitled"
        category = grievance["category"] or "Unknown"
        priority = grievance["priority"] or "Low"
        status = grievance["status"] or "Pending"
        severity = grievance["severity"] or "Medium"


        ctk.CTkLabel(
            top,
            text=f"GRV-{grievance_id:04d}",
            font=("Arial", 11, "bold"),
            text_color=AI_CYAN
        ).pack(
            side="left"
        )


        self.create_badge(
            top,
            priority,
            self.get_priority_color(priority)
        )

        self.create_badge(
            top,
            status,
            self.get_status_color(status)
        )


        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 16, "bold"),
            text_color=TEXT,
            anchor="w"
        )

        title_label.pack(
            fill="x",
            padx=18,
            pady=(5, 2)
        )


        # ----------------------------------------------------
        # INFORMATION
        # ----------------------------------------------------

        info = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        info.pack(
            fill="x",
            padx=18,
            pady=(5, 5)
        )

        ctk.CTkLabel(
            info,
            text=f"Category: {category}",
            font=("Arial", 11),
            text_color=MUTED
        ).pack(
            side="left",
            padx=(0, 25)
        )

        ctk.CTkLabel(
            info,
            text=f"Severity: {severity}",
            font=("Arial", 11),
            text_color=MUTED
        ).pack(
            side="left",
            padx=(0, 25)
        )

        ctk.CTkLabel(
            info,
            text=f"Location: {grievance['location'] or 'Not specified'}",
            font=("Arial", 11),
            text_color=MUTED
        ).pack(side="left")


        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        description = grievance["description"] or ""

        if len(description) > 180:
            description = description[:180] + "..."

        ctk.CTkLabel(
            card,
            text=description,
            font=("Arial", 11),
            text_color=TEXT,
            justify="left",
            anchor="w",
            wraplength=850
        ).pack(
            fill="x",
            padx=18,
            pady=(5, 8)
        )


        # ----------------------------------------------------
        # AI ANALYSIS
        # ----------------------------------------------------

        ai_reason = grievance["ai_reason"] or ""

        if ai_reason:

            ai_box = ctk.CTkFrame(
                card,
                fg_color="#0D1930",
                corner_radius=11,
                border_width=1,
                border_color="#27385E"
            )

            ai_box.pack(
                fill="x",
                padx=18,
                pady=(0, 10)
            )

            ctk.CTkLabel(
                ai_box,
                text="✦  AI Analysis",
                font=("Arial", 11, "bold"),
                text_color=AI_CYAN
            ).pack(
                anchor="w",
                padx=12,
                pady=(9, 3)
            )

            ctk.CTkLabel(
                ai_box,
                text=ai_reason,
                font=("Arial", 10),
                text_color=TEXT,
                justify="left",
                anchor="w",
                wraplength=850
            ).pack(
                fill="x",
                padx=12,
                pady=(0, 9)
            )


        # ----------------------------------------------------
        # BOTTOM CONTROLS
        # ----------------------------------------------------

        bottom = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        bottom.pack(
            fill="x",
            padx=18,
            pady=(0, 15)
        )

        ctk.CTkLabel(
            bottom,
            text=f"Submitted: {grievance['created_at'] or 'Unknown'}",
            font=("Arial", 10),
            text_color=MUTED
        ).pack(
            side="left"
        )


        status_menu = ctk.CTkComboBox(
            bottom,
            values=[
                "Pending",
                "In Progress",
                "Resolved"
            ],
            width=150,
            height=34,
            corner_radius=8,
            fg_color="#0C1122",
            border_color=BORDER,
            button_color=PRIMARY,
            button_hover_color=PRIMARY_HOVER,
            text_color=TEXT,
            dropdown_fg_color=CARD,
            dropdown_hover_color=CARD_HOVER,
            dropdown_text_color=TEXT
        )

        status_menu.set(status)

        status_menu.pack(
            side="right",
            padx=(8, 0)
        )


        ctk.CTkButton(
            bottom,
            text="Update Status",
            width=125,
            height=34,
            corner_radius=8,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=("Arial", 10, "bold"),
            command=lambda:
                self.change_status(
                    grievance_id,
                    status_menu.get()
                )
        ).pack(
            side="right"
        )


        # ----------------------------------------------------
        # CARD HOVER EFFECT
        # ----------------------------------------------------

        self.add_hover_effect(card)


    # ========================================================
    # CARD HOVER
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
    # BADGE
    # ========================================================

    def create_badge(
        self,
        parent,
        text,
        color
    ):

        badge = ctk.CTkLabel(
            parent,
            text=text,
            font=("Arial", 10, "bold"),
            text_color=color,
            fg_color="#0C1122",
            corner_radius=7,
            padx=9,
            pady=4
        )

        badge.pack(
            side="left",
            padx=5
        )


    # ========================================================
    # STATUS UPDATE
    # ========================================================

    def change_status(
        self,
        grievance_id,
        new_status
    ):

        update_status(
            grievance_id,
            new_status
        )

        self.load_grievances()


    # ========================================================
    # PRIORITY COLORS
    # ========================================================

    def get_priority_color(self, priority):

        colors = {
            "Critical": RED,
            "High": ORANGE,
            "Medium": BLUE,
            "Low": GREEN
        }

        return colors.get(
            priority,
            MUTED
        )


    # ========================================================
    # STATUS COLORS
    # ========================================================

    def get_status_color(self, status):

        colors = {
            "Pending": ORANGE,
            "In Progress": BLUE,
            "Resolved": GREEN
        }

        return colors.get(
            status,
            MUTED
        )