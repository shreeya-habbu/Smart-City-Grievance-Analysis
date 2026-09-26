import customtkinter as ctk

from database import initialize_database
from grievance import GrievancePage
from dashboard import DashboardPage
from grievance_management import GrievanceManagementPage
from track_grievance import TrackGrievancePage
from ai_insights import AIInsightsPage
from analytics import AnalyticsPage


# ============================================================
# COSMIC SMART CITY THEME
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Main colors
APP_BG = "#080B1A"
SIDEBAR = "#0D1224"
SIDEBAR_BORDER = "#1D2745"

PRIMARY = "#7C4DFF"
PRIMARY_HOVER = "#936BFF"

SECONDARY = "#A970FF"
AI_CYAN = "#4DD9FF"

SUCCESS = "#55D6A5"
WARNING = "#FFB84D"
CRITICAL = "#FF647C"

CARD = "#11172B"
CARD_HOVER = "#18213D"

TEXT = "#F4F2FF"
MUTED = "#9299B5"
MUTED_DARK = "#68708D"

BORDER = "#202A48"


# ============================================================
# MAIN APPLICATION
# ============================================================

class SmartCityApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Smart City Grievance Analysis")
        self.geometry("1280x760")
        self.minsize(1050, 650)

        self.configure(
            fg_color=APP_BG
        )

        # Initialize database
        initialize_database()

        # Build interface
        self.create_layout()

        # Start dashboard
        self.show_dashboard()

        # Start subtle brand animation
        self.start_brand_animation()


    # ========================================================
    # MAIN LAYOUT
    # ========================================================

    def create_layout(self):

        # ----------------------------------------------------
        # SIDEBAR
        # ----------------------------------------------------

        self.sidebar = ctk.CTkFrame(
            self,
            width=245,
            fg_color=SIDEBAR,
            corner_radius=0,
            border_width=1,
            border_color=SIDEBAR_BORDER
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)


        # ----------------------------------------------------
        # BRAND
        # ----------------------------------------------------

        brand = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        brand.pack(
            fill="x",
            padx=20,
            pady=(25, 28)
        )


        # Logo circle
        self.logo_frame = ctk.CTkFrame(
            brand,
            width=48,
            height=48,
            corner_radius=15,
            fg_color="#181333",
            border_width=1,
            border_color="#49328C"
        )

        self.logo_frame.pack(
            side="left"
        )

        self.logo_frame.pack_propagate(False)


        self.logo_label = ctk.CTkLabel(
            self.logo_frame,
            text="✦",
            font=("Arial", 27, "bold"),
            text_color=AI_CYAN
        )

        self.logo_label.pack(
            expand=True
        )


        # Brand text
        brand_text = ctk.CTkFrame(
            brand,
            fg_color="transparent"
        )

        brand_text.pack(
            side="left",
            padx=11
        )


        ctk.CTkLabel(
            brand_text,
            text="SmartCity",
            font=("Arial", 20, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w"
        )


        ctk.CTkLabel(
            brand_text,
            text="AI Grievance Intelligence",
            font=("Arial", 9),
            text_color=AI_CYAN
        ).pack(
            anchor="w",
            pady=(2, 0)
        )


        # ----------------------------------------------------
        # SYSTEM STATUS
        # ----------------------------------------------------

        status_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="#0F1930",
            corner_radius=12,
            border_width=1,
            border_color="#1C3150"
        )

        status_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 22)
        )


        status_dot = ctk.CTkLabel(
            status_frame,
            text="●",
            font=("Arial", 12),
            text_color=SUCCESS
        )

        status_dot.pack(
            side="left",
            padx=(13, 5),
            pady=10
        )


        ctk.CTkLabel(
            status_frame,
            text="AI SYSTEM ONLINE",
            font=("Arial", 9, "bold"),
            text_color=SUCCESS
        ).pack(
            side="left",
            pady=10
        )


        # ----------------------------------------------------
        # NAVIGATION TITLE
        # ----------------------------------------------------

        ctk.CTkLabel(
            self.sidebar,
            text="COMMAND CENTER",
            font=("Arial", 9, "bold"),
            text_color=MUTED_DARK
        ).pack(
            anchor="w",
            padx=24,
            pady=(0, 9)
        )


        # ----------------------------------------------------
        # NAVIGATION BUTTONS
        # ----------------------------------------------------

        self.dashboard_button = self.create_nav_button(
            "▣   Dashboard",
            self.show_dashboard
        )

        self.grievance_button = self.create_nav_button(
            "＋   Submit Grievance",
            self.show_grievance
        )

        self.management_button = self.create_nav_button(
            "▤   Manage Grievances",
            self.show_management
        )

        self.track_button = self.create_nav_button(
            "⌕   Track Grievance",
            self.show_tracking
        )

        self.analytics_button = self.create_nav_button(
            "◈   Analytics",
            self.show_analytics
        )

        self.ai_button = self.create_nav_button(
            "✦   AI Insights",
            self.show_ai_insights
        )


        # ----------------------------------------------------
        # BOTTOM SECTION
        # ----------------------------------------------------

        bottom = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        bottom.pack(
            side="bottom",
            fill="x",
            padx=18,
            pady=20
        )


        # Divider
        ctk.CTkFrame(
            bottom,
            height=1,
            fg_color=BORDER
        ).pack(
            fill="x",
            pady=(0, 15)
        )


        # SDG badge
        sdg_badge = ctk.CTkFrame(
            bottom,
            fg_color="#16112C",
            corner_radius=12,
            border_width=1,
            border_color="#30215D"
        )

        sdg_badge.pack(
            fill="x"
        )


        ctk.CTkLabel(
            sdg_badge,
            text="SDG 11",
            font=("Arial", 12, "bold"),
            text_color=PRIMARY
        ).pack(
            anchor="w",
            padx=13,
            pady=(11, 1)
        )


        ctk.CTkLabel(
            sdg_badge,
            text="Sustainable Cities & Communities",
            font=("Arial", 9),
            text_color=MUTED,
            wraplength=175,
            justify="left"
        ).pack(
            anchor="w",
            padx=13,
            pady=(0, 10)
        )


        ctk.CTkLabel(
            bottom,
            text="AI-assisted  •  Human reviewed",
            font=("Arial", 8),
            text_color=MUTED_DARK
        ).pack(
            anchor="w",
            padx=3,
            pady=(10, 0)
        )


        # ----------------------------------------------------
        # CONTENT AREA
        # ----------------------------------------------------

        self.content = ctk.CTkFrame(
            self,
            fg_color=APP_BG,
            corner_radius=0
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )


    # ========================================================
    # NAVIGATION BUTTON
    # ========================================================

    def create_nav_button(self, text, command):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=47,
            corner_radius=12,
            fg_color="transparent",
            hover_color=CARD_HOVER,
            text_color=MUTED,
            anchor="w",
            font=("Arial", 13),
            border_width=0,
            command=command
        )

        button.pack(
            fill="x",
            padx=12,
            pady=3
        )

        return button


    # ========================================================
    # CLEAR CONTENT
    # ========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()


    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.clear_content()

        page = DashboardPage(
            self.content
        )

        page.pack(
            fill="both",
            expand=True
        )

        self.set_active(
            self.dashboard_button
        )


    # ========================================================
    # GRIEVANCE
    # ========================================================

    def show_grievance(self):

        self.clear_content()

        page = GrievancePage(
            self.content,
            on_back=self.show_dashboard
        )

        page.pack(
            fill="both",
            expand=True
        )

        self.set_active(
            self.grievance_button
        )


    # ========================================================
    # MANAGEMENT
    # ========================================================

    def show_management(self):

        self.clear_content()

        page = GrievanceManagementPage(
            self.content,
            on_back=self.show_dashboard
        )

        page.pack(
            fill="both",
            expand=True
        )

        self.set_active(
            self.management_button
        )


    # ========================================================
    # TRACKING
    # ========================================================

    def show_tracking(self):

        self.clear_content()

        page = TrackGrievancePage(
            self.content,
            on_back=self.show_dashboard
        )

        page.pack(
            fill="both",
            expand=True
        )

        self.set_active(
            self.track_button
        )


    # ========================================================
    # AI INSIGHTS
    # ========================================================

    def show_ai_insights(self):

        self.clear_content()

        page = AIInsightsPage(
            self.content,
            on_back=self.show_dashboard
        )

        page.pack(
            fill="both",
            expand=True
        )

        self.set_active(
            self.ai_button
        )


    # ========================================================
    # ANALYTICS
    # ========================================================

    def show_analytics(self):

        self.clear_content()

        page = AnalyticsPage(
            self.content,
            on_back=self.show_dashboard
        )

        page.pack(
            fill="both",
            expand=True
        )

        self.set_active(
            self.analytics_button
        )


    # ========================================================
    # ACTIVE NAVIGATION
    # ========================================================

    def set_active(self, active_button):

        buttons = [
            self.dashboard_button,
            self.grievance_button,
            self.management_button,
            self.track_button,
            self.analytics_button,
            self.ai_button
        ]

        for button in buttons:

            if button == active_button:

                button.configure(
                    fg_color="#211547",
                    hover_color="#2C1C5C",
                    text_color=TEXT
                )

            else:

                button.configure(
                    fg_color="transparent",
                    hover_color=CARD_HOVER,
                    text_color=MUTED
                )


    # ========================================================
    # SUBTLE BRAND ANIMATION
    # ========================================================

    def start_brand_animation(self):

        self.animate_logo(True)


    def animate_logo(self, state):

        if not self.winfo_exists():
            return

        if state:

            self.logo_label.configure(
                text_color=AI_CYAN
            )

        else:

            self.logo_label.configure(
                text_color=SECONDARY
            )

        self.after(
            1400,
            lambda: self.animate_logo(not state)
        )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    app = SmartCityApp()

    app.mainloop()