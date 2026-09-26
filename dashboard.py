
import customtkinter as ctk
from collections import Counter

from database import get_all_grievances, get_statistics


# ============================================================
# COSMIC SMART CITY THEME
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
MUTED_DARK = "#68708D"

BORDER = "#202A48"
BORDER_HOVER = "#5940A8"

GREEN = "#55D6A5"
ORANGE = "#FFB84D"
RED = "#FF647C"
BLUE = "#5EAFFF"


# ============================================================
# DASHBOARD PAGE
# ============================================================

class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color=BG
        )

        self.create_dashboard()


    # ========================================================
    # MAIN DASHBOARD
    # ========================================================

    def create_dashboard(self):

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

        title_frame.pack(
            side="left"
        )

        ctk.CTkLabel(
            title_frame,
            text="Smart City Dashboard",
            font=("Arial", 27, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            title_frame,
            text="AI-powered civic intelligence and grievance monitoring",
            font=("Arial", 11),
            text_color=MUTED
        ).pack(
            anchor="w",
            pady=(4, 0)
        )


        # ----------------------------------------------------
        # REFRESH BUTTON
        # ----------------------------------------------------

        self.refresh_button = ctk.CTkButton(
            header,
            text="↻  Refresh",
            width=115,
            height=40,
            corner_radius=11,
            fg_color="#211547",
            hover_color="#34216B",
            border_width=1,
            border_color="#3A286F",
            text_color=TEXT,
            font=("Arial", 11, "bold"),
            command=self.refresh
        )

        self.refresh_button.pack(
            side="right"
        )


        # ----------------------------------------------------
        # LIVE STATUS
        # ----------------------------------------------------

        live_frame = ctk.CTkFrame(
            header,
            fg_color="#0D1827",
            corner_radius=10,
            border_width=1,
            border_color="#18364A"
        )

        live_frame.pack(
            side="right",
            padx=(0, 12)
        )

        self.live_dot = ctk.CTkLabel(
            live_frame,
            text="●",
            font=("Arial", 10),
            text_color=GREEN
        )

        self.live_dot.pack(
            side="left",
            padx=(10, 4),
            pady=9
        )

        ctk.CTkLabel(
            live_frame,
            text="LIVE",
            font=("Arial", 9, "bold"),
            text_color=GREEN
        ).pack(
            side="left",
            padx=(0, 10)
        )

        self.animate_live_dot(True)


        # ----------------------------------------------------
        # STATISTICS
        # ----------------------------------------------------

        self.stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.stats_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        self.create_stat_cards()


        # ----------------------------------------------------
        # AI INSIGHT
        # ----------------------------------------------------

        self.create_ai_insight()


        # ----------------------------------------------------
        # ANALYTICS
        # ----------------------------------------------------

        self.create_analytics()


        # ----------------------------------------------------
        # RECENT GRIEVANCES
        # ----------------------------------------------------

        self.create_recent_grievances()


    # ========================================================
    # STATISTIC CARDS
    # ========================================================

    def create_stat_cards(self):

        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        stats = get_statistics()

        cards = [
            (
                "Total Grievances",
                stats.get("total", 0),
                PRIMARY,
                "▣"
            ),
            (
                "Pending",
                stats.get("pending", 0),
                ORANGE,
                "◷"
            ),
            (
                "In Progress",
                stats.get("in_progress", 0),
                BLUE,
                "⚙"
            ),
            (
                "Resolved",
                stats.get("resolved", 0),
                GREEN,
                "✓"
            )
        ]

        for title, value, color, icon in cards:

            card = ctk.CTkFrame(
                self.stats_frame,
                fg_color=CARD,
                corner_radius=16,
                border_width=1,
                border_color=BORDER
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=6
            )

            # Hover effect
            self.add_card_hover(
                card,
                CARD,
                CARD_HOVER
            )


            # Icon
            icon_label = ctk.CTkLabel(
                card,
                text=icon,
                font=("Arial", 23),
                text_color=color
            )

            icon_label.pack(
                anchor="w",
                padx=18,
                pady=(13, 0)
            )


            # Animated number
            number_label = ctk.CTkLabel(
                card,
                text="0",
                font=("Arial", 27, "bold"),
                text_color=TEXT
            )

            number_label.pack(
                anchor="w",
                padx=18,
                pady=(1, 0)
            )


            # Title
            ctk.CTkLabel(
                card,
                text=title,
                font=("Arial", 10),
                text_color=MUTED
            ).pack(
                anchor="w",
                padx=18,
                pady=(0, 13)
            )


            self.animate_number(
                number_label,
                value
            )


    # ========================================================
    # NUMBER ANIMATION
    # ========================================================

    def animate_number(self, label, target, current=0):

        if current >= target:

            label.configure(
                text=str(target)
            )

            return

        step = max(
            1,
            int(target / 12)
        )

        current = min(
            current + step,
            target
        )

        label.configure(
            text=str(current)
        )

        label.after(
            45,
            lambda: self.animate_number(
                label,
                target,
                current
            )
        )


    # ========================================================
    # AI INSIGHT
    # ========================================================

    def create_ai_insight(self):

        grievances = get_all_grievances()

        card = ctk.CTkFrame(
            self,
            fg_color="#12132E",
            corner_radius=16,
            border_width=1,
            border_color="#342D68"
        )

        card.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        # Left AI indicator
        indicator = ctk.CTkFrame(
            card,
            width=5,
            height=55,
            corner_radius=3,
            fg_color=AI_CYAN
        )

        indicator.pack(
            side="left",
            padx=(12, 0),
            pady=10
        )


        # AI icon
        self.ai_icon = ctk.CTkLabel(
            card,
            text="✦",
            font=("Arial", 20, "bold"),
            text_color=AI_CYAN
        )

        self.ai_icon.pack(
            side="left",
            padx=(14, 8),
            pady=15
        )


        ctk.CTkLabel(
            card,
            text="AI INSIGHT",
            font=("Arial", 9, "bold"),
            text_color=AI_CYAN
        ).pack(
            side="left",
            padx=(0, 12),
            pady=15
        )


        if grievances:

            categories = [
                g["category"]
                if g["category"]
                else "Unknown"
                for g in grievances
            ]

            most_common = Counter(
                categories
            ).most_common(1)

            if most_common:

                category = most_common[0][0]
                count = most_common[0][1]

                message = (
                    f"{category} currently has the highest "
                    f"number of reported grievances ({count})."
                )

            else:

                message = (
                    "AI insights will appear as more "
                    "grievances are submitted."
                )

        else:

            message = (
                "Submit grievances to generate "
                "AI-powered insights."
            )


        ctk.CTkLabel(
            card,
            text=message,
            font=("Arial", 11),
            text_color=TEXT
        ).pack(
            side="left",
            padx=5,
            pady=15
        )


        # Animate AI icon
        self.animate_ai_icon(True)


    # ========================================================
    # AI ICON ANIMATION
    # ========================================================

    def animate_ai_icon(self, state):

        if not self.winfo_exists():
            return

        if state:

            self.ai_icon.configure(
                text_color=AI_CYAN
            )

        else:

            self.ai_icon.configure(
                text_color=SECONDARY
            )

        self.after(
            900,
            lambda: self.animate_ai_icon(not state)
        )


    # ========================================================
    # ANALYTICS
    # ========================================================

    def create_analytics(self):

        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        container.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        self.create_category_chart(
            container
        )

        self.create_priority_chart(
            container
        )


    # ========================================================
    # CATEGORY CHART
    # ========================================================

    def create_category_chart(self, parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )

        self.add_card_hover(
            card,
            CARD,
            CARD_HOVER
        )


        ctk.CTkLabel(
            card,
            text="Grievances by Category",
            font=("Arial", 15, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 10)
        )


        grievances = get_all_grievances()

        categories = [
            g["category"]
            if g["category"]
            else "Unknown"
            for g in grievances
        ]

        counts = Counter(categories)


        if not counts:

            ctk.CTkLabel(
                card,
                text="No data available",
                text_color=MUTED
            ).pack(
                pady=35
            )

            return


        max_value = max(
            counts.values()
        )


        for category, count in counts.items():

            row = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=18,
                pady=4
            )


            ctk.CTkLabel(
                row,
                text=category,
                width=150,
                anchor="w",
                font=("Arial", 10),
                text_color=TEXT
            ).pack(
                side="left"
            )


            bar_background = ctk.CTkFrame(
                row,
                height=18,
                fg_color="#1C2440",
                corner_radius=9
            )

            bar_background.pack(
                side="left",
                fill="x",
                expand=True,
                padx=5
            )

            bar_background.pack_propagate(False)


            bar = ctk.CTkFrame(
                bar_background,
                height=18,
                fg_color=PRIMARY,
                corner_radius=9
            )

            bar.pack(
                side="left",
                fill="y"
            )

            self.animate_bar(
                bar,
                bar_background,
                count,
                max_value
            )


            ctk.CTkLabel(
                row,
                text=str(count),
                width=30,
                font=("Arial", 10, "bold"),
                text_color=SECONDARY
            ).pack(
                side="right"
            )


    # ========================================================
    # ANIMATED BAR
    # ========================================================

    def animate_bar(
        self,
        bar,
        background,
        count,
        maximum,
        current=0
    ):

        target = max(
            20,
            int(
                (count / maximum)
                * 180
            )
        )

        if current >= target:

            bar.configure(
                width=target
            )

            return


        current += max(
            5,
            int(target / 10)
        )

        current = min(
            current,
            target
        )

        bar.configure(
            width=current
        )

        bar.after(
            30,
            lambda: self.animate_bar(
                bar,
                background,
                count,
                maximum,
                current
            )
        )


    # ========================================================
    # PRIORITY CHART
    # ========================================================

    def create_priority_chart(self, parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(7, 0)
        )

        self.add_card_hover(
            card,
            CARD,
            CARD_HOVER
        )


        ctk.CTkLabel(
            card,
            text="Priority Distribution",
            font=("Arial", 15, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 10)
        )


        grievances = get_all_grievances()


        # FIXED:
        # Previously this incorrectly used category.
        priorities = [
            g["priority"]
            if g["priority"]
            else "Unknown"
            for g in grievances
        ]


        counts = Counter(
            priorities
        )


        order = [
            ("Critical", RED),
            ("High", ORANGE),
            ("Medium", BLUE),
            ("Low", GREEN)
        ]


        if not counts:

            ctk.CTkLabel(
                card,
                text="No data available",
                text_color=MUTED
            ).pack(
                pady=35
            )

            return


        total = len(
            priorities
        )


        for priority, color in order:

            count = counts.get(
                priority,
                0
            )


            percentage = (
                (count / total) * 100
                if total > 0
                else 0
            )


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
                text=priority,
                width=80,
                anchor="w",
                font=("Arial", 10, "bold"),
                text_color=color
            ).pack(
                side="left"
            )


            bar_background = ctk.CTkFrame(
                row,
                height=18,
                fg_color="#1C2440",
                corner_radius=9
            )

            bar_background.pack(
                side="left",
                fill="x",
                expand=True,
                padx=5
            )

            bar_background.pack_propagate(False)


            bar = ctk.CTkFrame(
                bar_background,
                height=18,
                fg_color=color,
                corner_radius=9
            )

            bar.pack(
                side="left",
                fill="y"
            )


            target = max(
                5,
                int(
                    (percentage / 100)
                    * 180
                )
            )


            self.animate_percentage_bar(
                bar,
                target
            )


            ctk.CTkLabel(
                row,
                text=f"{count} ({percentage:.0f}%)",
                width=65,
                font=("Arial", 10),
                text_color=TEXT
            ).pack(
                side="right"
            )


    # ========================================================
    # PERCENTAGE BAR ANIMATION
    # ========================================================

    def animate_percentage_bar(
        self,
        bar,
        target,
        current=0
    ):

        if current >= target:

            bar.configure(
                width=target
            )

            return


        current += max(
            4,
            int(target / 10)
        )

        current = min(
            current,
            target
        )


        bar.configure(
            width=current
        )


        bar.after(
            30,
            lambda: self.animate_percentage_bar(
                bar,
                target,
                current
            )
        )


    # ========================================================
    # RECENT GRIEVANCES
    # ========================================================

    def create_recent_grievances(self):

        card = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )


        self.add_card_hover(
            card,
            CARD,
            CARD_HOVER
        )


        ctk.CTkLabel(
            card,
            text="Recent Grievances",
            font=("Arial", 15, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 8)
        )


        grievances = get_all_grievances()


        if not grievances:

            ctk.CTkLabel(
                card,
                text="No grievances submitted yet.",
                text_color=MUTED
            ).pack(
                pady=20
            )

            return


        recent = grievances[-5:]

        recent.reverse()


        for grievance in recent:

            row = ctk.CTkFrame(
                card,
                fg_color="#0D1326",
                corner_radius=10,
                border_width=1,
                border_color="#18213B"
            )

            row.pack(
                fill="x",
                padx=15,
                pady=4
            )


            self.add_card_hover(
                row,
                "#0D1326",
                "#17213A"
            )


            grievance_id = grievance["id"]

            title = (
                grievance["title"]
                or "Untitled"
            )

            category = (
                grievance["category"]
                or "Unknown"
            )

            priority = (
                grievance["priority"]
                or "Unknown"
            )

            status = (
                grievance["status"]
                or "Pending"
            )


            ctk.CTkLabel(
                row,
                text=f"GRV-{int(grievance_id):04d}",
                width=90,
                font=("Arial", 10, "bold"),
                text_color=SECONDARY
            ).pack(
                side="left",
                padx=10,
                pady=10
            )


            ctk.CTkLabel(
                row,
                text=title,
                font=("Arial", 11, "bold"),
                text_color=TEXT
            ).pack(
                side="left",
                padx=10
            )


            ctk.CTkLabel(
                row,
                text=category,
                font=("Arial", 10),
                text_color=MUTED
            ).pack(
                side="left",
                padx=10
            )


            status_color = (
                GREEN
                if status == "Resolved"
                else BLUE
                if status == "In Progress"
                else ORANGE
            )


            ctk.CTkLabel(
                row,
                text=status,
                font=("Arial", 10, "bold"),
                text_color=status_color
            ).pack(
                side="right",
                padx=10
            )


            priority_color = (
                RED
                if priority == "Critical"
                else ORANGE
                if priority == "High"
                else BLUE
                if priority == "Medium"
                else MUTED
            )


            ctk.CTkLabel(
                row,
                text=priority,
                font=("Arial", 10, "bold"),
                text_color=priority_color
            ).pack(
                side="right",
                padx=10
            )


    # ========================================================
    # CARD HOVER EFFECT
    # ========================================================

    def add_card_hover(
        self,
        widget,
        normal_color,
        hover_color
    ):

        def enter(event):

            try:

                widget.configure(
                    fg_color=hover_color,
                    border_color=BORDER_HOVER
                )

            except Exception:
                pass


        def leave(event):

            try:

                widget.configure(
                    fg_color=normal_color,
                    border_color=BORDER
                )

            except Exception:
                pass


        widget.bind(
            "<Enter>",
            enter,
            add="+"
        )

        widget.bind(
            "<Leave>",
            leave,
            add="+"
        )


    # ========================================================
    # LIVE DOT ANIMATION
    # ========================================================

    def animate_live_dot(self, state):

        if not self.winfo_exists():
            return

        try:

            if state:

                self.live_dot.configure(
                    text_color=GREEN
                )

            else:

                self.live_dot.configure(
                    text_color="#245F4A"
                )

            self.after(
                700,
                lambda: self.animate_live_dot(
                    not state
                )
            )

        except Exception:
            pass


    # ========================================================
    # REFRESH
    # ========================================================

    def refresh(self):

        try:

            self.refresh_button.configure(
                text="⟳  Updating...",
                state="disabled"
            )

            self.update()

            self.after(
                250,
                self.finish_refresh
            )

        except Exception:
            self.finish_refresh()


    def finish_refresh(self):

        for widget in self.winfo_children():
            widget.destroy()

        self.create_dashboard()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    root = ctk.CTk()

    root.geometry(
        "1280x760"
    )

    DashboardPage(
        root
    ).pack(
        fill="both",
        expand=True
    )

    root.mainloop()

