import customtkinter as ctk

from database import get_all_grievances


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
# ANALYTICS PAGE
# ============================================================

class AnalyticsPage(ctk.CTkFrame):

    def __init__(self, parent, on_back=None):

        super().__init__(
            parent,
            fg_color=BG
        )

        self.on_back = on_back
        self.all_grievances = []

        self.create_page()
        self.load_analytics()


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
            text="Analytics & Insights",
            font=("Arial", 27, "bold"),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Understand grievance patterns and service performance",
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
            command=self.load_analytics
        )

        self.refresh_button.pack(side="right")


        # ----------------------------------------------------
        # SCROLLABLE CONTENT
        # ----------------------------------------------------

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#252E4B",
            scrollbar_button_hover_color=PRIMARY
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )


    # ========================================================
    # LOAD ANALYTICS
    # ========================================================

    def load_analytics(self):

        self.refresh_button.configure(
            text="Updating...",
            state="disabled"
        )

        self.after(
            100,
            self._build_analytics
        )


    def _build_analytics(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        self.all_grievances = get_all_grievances()

        self.refresh_button.configure(
            text="⟳  Refresh",
            state="normal"
        )

        if not self.all_grievances:
            self.show_empty_state()
            return

        grievances = self.all_grievances

        total = len(grievances)

        pending = sum(
            1
            for g in grievances
            if (g["status"] or "Pending") == "Pending"
        )

        in_progress = sum(
            1
            for g in grievances
            if (g["status"] or "Pending") == "In Progress"
        )

        resolved = sum(
            1
            for g in grievances
            if (g["status"] or "Pending") == "Resolved"
        )


        # ----------------------------------------------------
        # DISTRIBUTIONS
        # ----------------------------------------------------

        categories = {}

        priorities = {}

        severities = {}

        statuses = {}

        for grievance in grievances:

            category = (
                grievance["category"]
                or "Unknown"
            )

            priority = (
                grievance["priority"]
                or "Unknown"
            )

            severity = (
                grievance["severity"]
                or "Unknown"
            )

            status = (
                grievance["status"]
                or "Pending"
            )

            categories[category] = (
                categories.get(category, 0) + 1
            )

            priorities[priority] = (
                priorities.get(priority, 0) + 1
            )

            severities[severity] = (
                severities.get(severity, 0) + 1
            )

            statuses[status] = (
                statuses.get(status, 0) + 1
            )


        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        self.create_summary(
            total,
            pending,
            in_progress,
            resolved
        )


        # ----------------------------------------------------
        # STATUS OVERVIEW
        # ----------------------------------------------------

        self.create_distribution_card(
            "Status Distribution",
            statuses,
            {
                "Pending": ORANGE,
                "In Progress": BLUE,
                "Resolved": GREEN
            }
        )


        # ----------------------------------------------------
        # CATEGORY
        # ----------------------------------------------------

        self.create_distribution_card(
            "Grievance Categories",
            categories,
            {
                "Roads & Transport": PRIMARY,
                "Water & Sanitation": AI_CYAN,
                "Electricity & Lighting": ORANGE,
                "Public Safety": RED,
                "Environment": GREEN,
                "Public Services": SECONDARY
            }
        )


        # ----------------------------------------------------
        # PRIORITY
        # ----------------------------------------------------

        self.create_distribution_card(
            "Priority Distribution",
            priorities,
            {
                "Critical": RED,
                "High": ORANGE,
                "Medium": BLUE,
                "Low": GREEN
            }
        )


        # ----------------------------------------------------
        # SEVERITY
        # ----------------------------------------------------

        self.create_distribution_card(
            "Severity Distribution",
            severities,
            {
                "Critical": RED,
                "High": ORANGE,
                "Medium": BLUE,
                "Low": GREEN
            }
        )


        # ----------------------------------------------------
        # PERFORMANCE
        # ----------------------------------------------------

        self.create_performance_card(
            total,
            pending,
            in_progress,
            resolved
        )


        # ----------------------------------------------------
        # RESPONSIBLE AI
        # ----------------------------------------------------

        self.create_responsible_ai()


    # ========================================================
    # SUMMARY CARDS
    # ========================================================

    def create_summary(
        self,
        total,
        pending,
        in_progress,
        resolved
    ):

        heading = ctk.CTkLabel(
            self.content,
            text="System Overview",
            font=("Arial", 16, "bold"),
            text_color=TEXT
        )

        heading.pack(
            anchor="w",
            pady=(0, 8)
        )


        row = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            pady=(0, 15)
        )


        self.create_stat_card(
            row,
            "TOTAL",
            total,
            PRIMARY
        )

        self.create_stat_card(
            row,
            "PENDING",
            pending,
            ORANGE
        )

        self.create_stat_card(
            row,
            "IN PROGRESS",
            in_progress,
            BLUE
        )

        self.create_stat_card(
            row,
            "RESOLVED",
            resolved,
            GREEN
        )


    # ========================================================
    # STAT CARD
    # ========================================================

    def create_stat_card(
        self,
        parent,
        label,
        value,
        accent
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )


        ctk.CTkFrame(
            card,
            width=5,
            height=65,
            fg_color=accent,
            corner_radius=4
        ).pack(
            side="left",
            padx=(12, 10),
            pady=12
        )


        text_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        text_frame.pack(
            side="left",
            pady=10
        )


        ctk.CTkLabel(
            text_frame,
            text=label,
            font=("Arial", 9, "bold"),
            text_color=MUTED
        ).pack(anchor="w")


        ctk.CTkLabel(
            text_frame,
            text=str(value),
            font=("Arial", 23, "bold"),
            text_color=TEXT
        ).pack(anchor="w")


        self.add_hover_effect(card)


    # ========================================================
    # DISTRIBUTION CARD
    # ========================================================

    def create_distribution_card(
        self,
        title,
        data,
        color_map
    ):

        card = ctk.CTkFrame(
            self.content,
            fg_color=CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="x",
            pady=7
        )


        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 16, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 5)
        )


        if not data:

            ctk.CTkLabel(
                card,
                text="No data available.",
                font=("Arial", 11),
                text_color=MUTED
            ).pack(
                anchor="w",
                padx=18,
                pady=(5, 18)
            )

            return


        max_value = max(
            data.values()
        )


        sorted_data = sorted(
            data.items(),
            key=lambda item: item[1],
            reverse=True
        )


        for name, count in sorted_data:

            row = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=18,
                pady=5
            )


            ctk.CTkLabel(
                row,
                text=name,
                width=185,
                anchor="w",
                font=("Arial", 10),
                text_color=TEXT
            ).pack(
                side="left"
            )


            bar_background = ctk.CTkFrame(
                row,
                height=12,
                fg_color="#0C1122",
                corner_radius=6
            )

            bar_background.pack(
                side="left",
                fill="x",
                expand=True,
                padx=10
            )


            bar = ctk.CTkFrame(
                bar_background,
                height=12,
                fg_color=color_map.get(
                    name,
                    PRIMARY
                ),
                corner_radius=6
            )

            bar.place(
                relx=0,
                rely=0,
                relheight=1,
                relwidth=0
            )


            percentage = (
                count / max_value
            )


            self.animate_bar(
                bar,
                percentage
            )


            ctk.CTkLabel(
                row,
                text=str(count),
                width=40,
                font=("Arial", 10, "bold"),
                text_color=TEXT
            ).pack(
                side="right"
            )


        ctk.CTkFrame(
            card,
            height=8,
            fg_color="transparent"
        ).pack()


        self.add_hover_effect(card)


    # ========================================================
    # ANIMATED BAR
    # ========================================================

    def animate_bar(
        self,
        bar,
        target,
        step=0
    ):

        if not bar.winfo_exists():
            return

        if step >= 20:

            bar.place_configure(
                relwidth=target
            )

            return


        current = (
            target * step / 20
        )

        bar.place_configure(
            relwidth=current
        )

        self.after(
            20,
            lambda: self.animate_bar(
                bar,
                target,
                step + 1
            )
        )


    # ========================================================
    # PERFORMANCE CARD
    # ========================================================

    def create_performance_card(
        self,
        total,
        pending,
        in_progress,
        resolved
    ):

        card = ctk.CTkFrame(
            self.content,
            fg_color=CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="x",
            pady=7
        )


        ctk.CTkLabel(
            card,
            text="Resolution Performance",
            font=("Arial", 16, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 4)
        )


        if total > 0:

            resolution_rate = (
                resolved / total
            ) * 100

        else:

            resolution_rate = 0


        ctk.CTkLabel(
            card,
            text=f"{resolution_rate:.1f}% resolved",
            font=("Arial", 24, "bold"),
            text_color=GREEN
        ).pack(
            anchor="w",
            padx=18,
            pady=(4, 2)
        )


        ctk.CTkLabel(
            card,
            text=(
                f"{resolved} resolved  •  "
                f"{in_progress} in progress  •  "
                f"{pending} pending"
            ),
            font=("Arial", 11),
            text_color=MUTED
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 10)
        )


        # Main progress bar

        progress_background = ctk.CTkFrame(
            card,
            height=14,
            fg_color="#0C1122",
            corner_radius=7
        )

        progress_background.pack(
            fill="x",
            padx=18,
            pady=(0, 18)
        )


        progress = ctk.CTkProgressBar(
            progress_background,
            height=14,
            corner_radius=7,
            fg_color="#0C1122",
            progress_color=GREEN
        )

        progress.pack(
            fill="both",
            expand=True
        )

        progress.set(
            resolution_rate / 100
        )


        self.add_hover_effect(card)


    # ========================================================
    # RESPONSIBLE AI
    # ========================================================

    def create_responsible_ai(self):

        card = ctk.CTkFrame(
            self.content,
            fg_color="#16152A",
            corner_radius=14,
            border_width=1,
            border_color="#302C55"
        )

        card.pack(
            fill="x",
            pady=10
        )


        ctk.CTkLabel(
            card,
            text="⚠  Responsible AI & Data Interpretation",
            font=("Arial", 12, "bold"),
            text_color=ORANGE
        ).pack(
            anchor="w",
            padx=18,
            pady=(13, 5)
        )


        ctk.CTkLabel(
            card,
            text=(
                "Analytics are generated from recorded grievances and "
                "are intended to support administrative decision-making. "
                "AI-generated insights should be reviewed by authorized "
                "human administrators before action is taken."
            ),
            font=("Arial", 10),
            text_color=MUTED,
            justify="left",
            anchor="w",
            wraplength=900
        ).pack(
            fill="x",
            padx=18,
            pady=(0, 13)
        )


    # ========================================================
    # EMPTY STATE
    # ========================================================

    def show_empty_state(self):

        card = ctk.CTkFrame(
            self.content,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="x",
            pady=15
        )


        ctk.CTkLabel(
            card,
            text="◌",
            font=("Arial", 40),
            text_color=PRIMARY
        ).pack(
            pady=(35, 5)
        )


        ctk.CTkLabel(
            card,
            text="No grievance data available",
            font=("Arial", 18, "bold"),
            text_color=TEXT
        ).pack(pady=(0, 5))


        ctk.CTkLabel(
            card,
            text=(
                "Submit a grievance to start generating analytics."
            ),
            font=("Arial", 11),
            text_color=MUTED
        ).pack(
            pady=(0, 35)
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