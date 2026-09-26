import customtkinter as ctk

from llm_service import analyze_with_gemini, is_configured
from rag.rag_engine import retrieve_context


# ============================================================
# COSMIC THEME
# ============================================================

BG = "#080B1A"
SIDEBAR = "#0D1224"
CARD = "#11172B"
CARD_HOVER = "#18213D"
PRIMARY = "#7C4DFF"
PRIMARY_HOVER = "#936BFF"
SECONDARY = "#A970FF"
AI_CYAN = "#4DD9FF"
SUCCESS = "#55D6A5"
WARNING = "#FFB84D"
CRITICAL = "#FF647C"
TEXT = "#F4F2FF"
MUTED = "#9299B5"
MUTED_DARK = "#68708D"
BORDER = "#202A48"


class AIInsightsPage(ctk.CTkFrame):

    def __init__(self, parent, on_back=None):
        super().__init__(parent, fg_color=BG)

        self.parent = parent
        self.on_back = on_back

        self.build_ui()

    # ========================================================
    # MAIN UI
    # ========================================================

    def build_ui(self):

        # Header
        header = ctk.CTkFrame(
            self,
            fg_color=BG,
            height=80
        )
        header.pack(fill="x", padx=30, pady=(20, 0))
        header.pack_propagate(False)

        # Back button
        back_button = ctk.CTkButton(
            header,
            text="←  Back",
            width=90,
            height=38,
            corner_radius=10,
            fg_color=CARD,
            hover_color=CARD_HOVER,
            border_width=1,
            border_color=BORDER,
            text_color=TEXT,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.go_back
        )
        back_button.pack(side="left", pady=15)

        # Title
        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )
        title_frame.pack(side="left", padx=20)

        ctk.CTkLabel(
            title_frame,
            text="AI Insights",
            text_color=TEXT,
            font=ctk.CTkFont(size=27, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Gemini AI + Retrieval-Augmented Generation",
            text_color=MUTED,
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", pady=(2, 0))

        # AI status
        status_text = "●  Gemini Connected" if is_configured() else "●  Gemini Not Configured"
        status_color = SUCCESS if is_configured() else WARNING

        self.status_label = ctk.CTkLabel(
            header,
            text=status_text,
            text_color=status_color,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.status_label.pack(side="right", padx=10)

        # Scrollable content
        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=BG,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=PRIMARY
        )
        self.scroll.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(5, 25)
        )

        self.build_content()

    # ========================================================
    # CONTENT
    # ========================================================

    def build_content(self):

        # ----------------------------------------------------
        # AI OVERVIEW CARD
        # ----------------------------------------------------

        overview = ctk.CTkFrame(
            self.scroll,
            fg_color=CARD,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )
        overview.pack(fill="x", pady=(5, 18))

        overview.grid_columnconfigure(1, weight=1)

        # AI icon
        icon = ctk.CTkLabel(
            overview,
            text="✦",
            width=65,
            height=65,
            corner_radius=18,
            fg_color="#1B1640",
            text_color=AI_CYAN,
            font=ctk.CTkFont(size=30, weight="bold")
        )
        icon.grid(row=0, column=0, rowspan=2, padx=22, pady=22)

        ctk.CTkLabel(
            overview,
            text="AI-Powered Grievance Intelligence",
            text_color=TEXT,
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(
            row=0,
            column=1,
            sticky="w",
            pady=(20, 2)
        )

        ctk.CTkLabel(
            overview,
            text=(
                "Gemini analyzes citizen grievances using retrieved civic "
                "knowledge from the RAG knowledge base."
            ),
            text_color=MUTED,
            font=ctk.CTkFont(size=12),
            wraplength=750,
            justify="left"
        ).grid(
            row=1,
            column=1,
            sticky="w",
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # RAG PIPELINE
        # ----------------------------------------------------

        ctk.CTkLabel(
            self.scroll,
            text="AI Processing Pipeline",
            text_color=TEXT,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", pady=(5, 10))

        pipeline = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )
        pipeline.pack(fill="x", pady=(0, 20))

        steps = [
            ("01", "Citizen Grievance", "User submits a complaint"),
            ("02", "RAG Retrieval", "Relevant civic knowledge is retrieved"),
            ("03", "Gemini AI", "LLM analyzes the grievance"),
            ("04", "AI Recommendation", "Category, priority & severity"),
            ("05", "Human Review", "Authorized admin reviews AI output")
        ]

        for index, (number, title, description) in enumerate(steps):

            step_card = ctk.CTkFrame(
                pipeline,
                fg_color=CARD,
                corner_radius=15,
                border_width=1,
                border_color=BORDER
            )

            step_card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=(0 if index == 0 else 5, 0 if index == len(steps) - 1 else 5)
            )

            ctk.CTkLabel(
                step_card,
                text=number,
                text_color=AI_CYAN,
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(
                anchor="w",
                padx=15,
                pady=(14, 3)
            )

            ctk.CTkLabel(
                step_card,
                text=title,
                text_color=TEXT,
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(
                anchor="w",
                padx=15
            )

            ctk.CTkLabel(
                step_card,
                text=description,
                text_color=MUTED,
                font=ctk.CTkFont(size=10),
                wraplength=140,
                justify="left"
            ).pack(
                anchor="w",
                padx=15,
                pady=(4, 15)
            )

        # ----------------------------------------------------
        # RAG KNOWLEDGE BASE
        # ----------------------------------------------------

        rag_card = ctk.CTkFrame(
            self.scroll,
            fg_color=CARD,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )
        rag_card.pack(fill="x", pady=(0, 18))

        ctk.CTkLabel(
            rag_card,
            text="◈  RAG Knowledge Base",
            text_color=AI_CYAN,
            font=ctk.CTkFont(size=17, weight="bold")
        ).pack(anchor="w", padx=22, pady=(18, 5))

        ctk.CTkLabel(
            rag_card,
            text=(
                "The system retrieves relevant civic information before "
                "sending the grievance to Gemini. This helps the LLM use "
                "project-specific knowledge instead of relying only on "
                "general model knowledge."
            ),
            text_color=MUTED,
            font=ctk.CTkFont(size=12),
            wraplength=900,
            justify="left"
        ).pack(anchor="w", padx=22, pady=(0, 15))

        knowledge_items = [
            "Grievance Handling",
            "Grievance Tracking",
            "Grievance Routing",
            "Roads & Transport",
            "Water & Sanitation",
            "Electricity & Lighting",
            "Environment & Waste",
            "Public Safety",
            "Human Oversight",
            "Responsible AI & Privacy"
        ]

        knowledge_frame = ctk.CTkFrame(
            rag_card,
            fg_color="transparent"
        )
        knowledge_frame.pack(fill="x", padx=18, pady=(0, 18))

        for index, item in enumerate(knowledge_items):

            row = index // 2
            column = index % 2

            badge = ctk.CTkFrame(
                knowledge_frame,
                fg_color="#0D1224",
                corner_radius=9,
                border_width=1,
                border_color=BORDER
            )

            badge.grid(
                row=row,
                column=column,
                sticky="ew",
                padx=5,
                pady=4
            )

            knowledge_frame.grid_columnconfigure(
                column,
                weight=1
            )

            ctk.CTkLabel(
                badge,
                text="✓  " + item,
                text_color=TEXT,
                font=ctk.CTkFont(size=11)
            ).pack(
                anchor="w",
                padx=12,
                pady=9
            )

        # ----------------------------------------------------
        # LIVE AI TEST
        # ----------------------------------------------------

        test_card = ctk.CTkFrame(
            self.scroll,
            fg_color=CARD,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )
        test_card.pack(fill="x", pady=(0, 18))

        ctk.CTkLabel(
            test_card,
            text="Test AI Analysis",
            text_color=TEXT,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=22, pady=(18, 3))

        ctk.CTkLabel(
            test_card,
            text="Enter a sample grievance to test Gemini + RAG.",
            text_color=MUTED,
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w", padx=22, pady=(0, 12))

        self.test_input = ctk.CTkTextbox(
            test_card,
            height=100,
            corner_radius=12,
            fg_color="#0D1224",
            border_width=1,
            border_color=BORDER,
            text_color=TEXT,
            font=ctk.CTkFont(size=12)
        )
        self.test_input.pack(
            fill="x",
            padx=22,
            pady=(0, 12)
        )

        self.test_input.insert(
            "1.0",
            "Garbage has not been collected for 5 days and waste is overflowing near the bus stop."
        )

        button_row = ctk.CTkFrame(
            test_card,
            fg_color="transparent"
        )
        button_row.pack(
            fill="x",
            padx=22,
            pady=(0, 15)
        )

        self.analyze_button = ctk.CTkButton(
            button_row,
            text="✦  Analyze with AI",
            width=170,
            height=40,
            corner_radius=10,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            text_color="white",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.run_analysis
        )
        self.analyze_button.pack(side="left")

        self.result_status = ctk.CTkLabel(
            button_row,
            text="",
            text_color=MUTED,
            font=ctk.CTkFont(size=11)
        )
        self.result_status.pack(side="left", padx=15)

        # Result area
        self.result_frame = ctk.CTkFrame(
            test_card,
            fg_color="#0D1224",
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )
        self.result_frame.pack(
            fill="x",
            padx=22,
            pady=(0, 20)
        )

        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="AI results will appear here.",
            text_color=MUTED_DARK,
            font=ctk.CTkFont(size=12),
            justify="left",
            anchor="w"
        )
        self.result_label.pack(
            fill="x",
            padx=18,
            pady=18
        )

        # ----------------------------------------------------
        # RESPONSIBLE AI
        # ----------------------------------------------------

        responsible = ctk.CTkFrame(
            self.scroll,
            fg_color="#101B25",
            corner_radius=18,
            border_width=1,
            border_color="#244A4A"
        )
        responsible.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            responsible,
            text="🛡  Responsible AI & Human Oversight",
            text_color=SUCCESS,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(
            anchor="w",
            padx=22,
            pady=(18, 5)
        )

        ctk.CTkLabel(
            responsible,
            text=(
                "AI-generated category, priority and severity are recommendations "
                "only. An authorized administrator should review important decisions. "
                "Citizens should provide only information necessary to process "
                "their grievance."
            ),
            text_color=MUTED,
            font=ctk.CTkFont(size=11),
            wraplength=900,
            justify="left"
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 18)
        )

    # ========================================================
    # AI ANALYSIS
    # ========================================================

    def run_analysis(self):

        grievance = self.test_input.get(
            "1.0",
            "end"
        ).strip()

        if not grievance:
            self.result_status.configure(
                text="Please enter a grievance.",
                text_color=WARNING
            )
            return

        if not is_configured():
            self.result_status.configure(
                text="Gemini is not configured.",
                text_color=WARNING
            )

            self.result_label.configure(
                text=(
                    "Gemini API is not configured.\n\n"
                    "The project can still use the local AI fallback "
                    "through the grievance submission page."
                ),
                text_color=WARNING
            )

            return

        self.analyze_button.configure(
            state="disabled",
            text="AI is analyzing..."
        )

        self.result_status.configure(
            text="Retrieving knowledge + analyzing...",
            text_color=AI_CYAN
        )

        self.result_label.configure(
            text="Processing grievance using RAG + Gemini...",
            text_color=AI_CYAN
        )

        self.update_idletasks()

        try:

            # --------------------------------------------
            # STEP 1: RAG retrieval
            # --------------------------------------------

            retrieved = retrieve_context(
                grievance,
                top_k=3
            )

            # --------------------------------------------
            # STEP 2: Gemini analysis
            # --------------------------------------------

            response = analyze_with_gemini(
                grievance
            )

            if response:

                self.show_analysis_result(
                    response,
                    retrieved
                )

            else:

                self.result_status.configure(
                    text="AI analysis failed.",
                    text_color=CRITICAL
                )

                self.result_label.configure(
                    text=(
                        "Gemini did not return a response.\n\n"
                        "Please try again."
                    ),
                    text_color=CRITICAL
                )

        except Exception as error:

            print("AI Insights error:", error)

            self.result_status.configure(
                text="Error during analysis.",
                text_color=CRITICAL
            )

            self.result_label.configure(
                text=(
                    "An error occurred while analyzing the grievance.\n\n"
                    f"Error: {error}"
                ),
                text_color=CRITICAL
            )

        finally:

            self.analyze_button.configure(
                state="normal",
                text="✦  Analyze with AI"
            )

    # ========================================================
    # SHOW RESULT
    # ========================================================

    def show_analysis_result(
        self,
        response,
        retrieved
    ):

        self.result_status.configure(
            text="✓ Analysis completed",
            text_color=SUCCESS
        )

        self.result_label.configure(
            text=response,
            text_color=TEXT,
            font=ctk.CTkFont(size=12),
            justify="left"
        )

        # RAG result information
        if retrieved:

            rag_text = "\n\n────────────────────────────\n"
            rag_text += "Retrieved RAG Knowledge\n\n"

            for item in retrieved:

                if isinstance(item, dict):

                    title = item.get(
                        "title",
                        "Knowledge Entry"
                    )

                    rag_text += f"• {title}\n"

                else:

                    rag_text += f"• {str(item)}\n"

            current_text = self.result_label.cget(
                "text"
            )

            self.result_label.configure(
                text=current_text + rag_text
            )

    # ========================================================
    # BACK
    # ========================================================

    def go_back(self):

        if self.on_back:
            self.on_back()