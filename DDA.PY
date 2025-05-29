import tkinter as tk
from tkinter import ttk, messagebox

CELL_SIZE = 32
UNITS_X = 18
UNITS_Y = 18

CANVAS_WIDTH = CELL_SIZE * UNITS_X
CANVAS_HEIGHT = CELL_SIZE * UNITS_Y

WORLD_X_MIN = -UNITS_X // 2
WORLD_Y_MIN = -UNITS_Y // 2
WORLD_X_MAX_EDGE = WORLD_X_MIN + UNITS_X
WORLD_Y_MAX_EDGE = WORLD_Y_MIN + UNITS_Y

BG_COLOR = "#F8F9FA"
INPUT_FRAME_BG_COLOR = "#FFFFFF"
CANVAS_OUTER_FRAME_BG_COLOR = "#E9ECEF"
INPUT_BG_COLOR = "#FFFFFF"
BUTTON_FG_COLOR = "#FFFFFF"
BUTTON_BG_COLOR = "#007BFF"
BUTTON_ACTIVE_BG_COLOR = "#0056B3"
TEXT_COLOR_PRIMARY = "#212529"
TEXT_COLOR_SECONDARY = "#6C757D"
GRID_COLOR = "#DEE2E6"
AXIS_COLOR = "#495057"
PIXEL_COLOR_DDA = "#007BFF"
IDEAL_LINE_COLOR = "#DC3545"
CANVAS_BG_COLOR = "#FFFFFF"
CELL_NUMBER_COLOR = "#ADB5BD"
CELL_NUMBER_AXIS_COLOR = "#495057"

FONT_FAMILY_PRIMARY = "Segoe UI"
FONT_FAMILY_FALLBACK = "Calibri"
FONT_SIZE_NORMAL = 11
FONT_SIZE_LABEL_FRAME = 12
FONT_SIZE_GRID_LABEL = 9
FONT_SIZE_CELL_NUMBER = 7


class DDAGraphicalTest:
    def __init__(self, master):
        self.master = master
        self._initialize_application()

    def _initialize_application(self):
        self._setup_window()
        self._setup_styles()
        self._create_interface()
        self._draw_initial_grid()

    def _setup_window(self):
        self.master.title("🎯 Visualizador DDA - Interface Aprimorada")
        self.master.configure(bg=BG_COLOR)
        self.master.resizable(False, False)

    def _setup_styles(self):
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except tk.TclError:
            self.style.theme_use('default')

        self._setup_fonts()
        self._configure_styles()

    def _setup_fonts(self):
        try:
            self.primary_font = (FONT_FAMILY_PRIMARY, FONT_SIZE_NORMAL)
            self.labelframe_font = (FONT_FAMILY_PRIMARY, FONT_SIZE_LABEL_FRAME, "bold")
            self.grid_label_font = (FONT_FAMILY_PRIMARY, FONT_SIZE_GRID_LABEL)
            self.cell_number_font = (FONT_FAMILY_PRIMARY, FONT_SIZE_CELL_NUMBER)
            self.button_font = (FONT_FAMILY_PRIMARY, FONT_SIZE_NORMAL, "bold")
        except tk.TclError:
            self.primary_font = (FONT_FAMILY_FALLBACK, FONT_SIZE_NORMAL)
            self.labelframe_font = (FONT_FAMILY_FALLBACK, FONT_SIZE_LABEL_FRAME, "bold")
            self.grid_label_font = (FONT_FAMILY_FALLBACK, FONT_SIZE_GRID_LABEL)
            self.cell_number_font = (FONT_FAMILY_FALLBACK, FONT_SIZE_CELL_NUMBER)
            self.button_font = (FONT_FAMILY_FALLBACK, FONT_SIZE_NORMAL, "bold")

    def _configure_styles(self):
        self.style.configure('.', font=self.primary_font, background=BG_COLOR, foreground=TEXT_COLOR_PRIMARY)
        
        self.style.configure('Input.TLabel', foreground=TEXT_COLOR_PRIMARY, background=INPUT_FRAME_BG_COLOR)
        self.style.configure('Outer.TLabel', foreground=TEXT_COLOR_SECONDARY, background=BG_COLOR)
        
        self.style.configure('TButton', font=self.button_font, foreground=BUTTON_FG_COLOR,
                             background=BUTTON_BG_COLOR, padding=(15, 10))
        self.style.map('TButton', background=[('active', BUTTON_ACTIVE_BG_COLOR), ('pressed', BUTTON_ACTIVE_BG_COLOR)])
        
        self.style.configure('TEntry', font=self.primary_font, fieldbackground=INPUT_BG_COLOR,
                             foreground=TEXT_COLOR_PRIMARY, padding=(8,8))
        
        self.style.configure('TLabelframe', labelmargins=(15, 5), background=INPUT_FRAME_BG_COLOR,
                             borderwidth=2, relief="solid")
        self.style.configure('TLabelframe.Label', font=self.labelframe_font, foreground=TEXT_COLOR_PRIMARY,
                             background=INPUT_FRAME_BG_COLOR)
        
        self.style.configure('CanvasOuter.TFrame', background=CANVAS_OUTER_FRAME_BG_COLOR)

    def _create_interface(self):
        self._create_header()
        self._create_input_section()
        self._create_action_button()
        self._create_visualization_area()
        self._create_information_footer()

    def _create_header(self):
        header_frame = ttk.Frame(self.master, style='TFrame')
        header_frame.pack(pady=(15, 5), padx=20, fill="x")
        
        title_label = ttk.Label(header_frame, text="Algoritmo DDA - Rasterização de Linha",
                               style='Outer.TLabel', font=(FONT_FAMILY_PRIMARY, 14, "bold"))
        title_label.pack()

    def _create_input_section(self):
        input_labelframe = ttk.LabelFrame(self.master, text="🎯 Coordenadas da Linha", 
                                         padding=(25, 20), style='TLabelframe')
        input_labelframe.pack(pady=15, padx=20, fill="x")

        self._setup_grid_weights(input_labelframe)
        self._create_coordinate_inputs(input_labelframe)

    def _setup_grid_weights(self, parent):
        for i in range(4):
            parent.grid_columnconfigure(i, weight=1 if i % 2 == 1 else 0)

    def _create_coordinate_inputs(self, parent):
        coordinates = [
            ("Ponto Inicial X:", "x0_entry", "-5", 0, 0),
            ("Ponto Inicial Y:", "y0_entry", "-4", 0, 2),
            ("Ponto Final X:", "x1_entry", "5", 1, 0),
            ("Ponto Final Y:", "y1_entry", "4", 1, 2)
        ]

        for label_text, attr_name, default_value, row, col in coordinates:
            ttk.Label(parent, text=label_text, style='Input.TLabel').grid(
                row=row, column=col, padx=(20 if col==2 else 0, 8), pady=10, sticky="w")
            
            entry = ttk.Entry(parent, width=10)
            entry.grid(row=row, column=col+1, pady=10, sticky="ew")
            entry.insert(0, default_value)
            setattr(self, attr_name, entry)

    def _create_action_button(self):
        button_frame = ttk.Frame(self.master, style='TFrame')
        button_frame.pack(pady=10, padx=20, fill="x")
        
        self.draw_button = ttk.Button(button_frame, text="🎨 Executar Algoritmo DDA", 
                                     command=self._execute_dda_algorithm)
        self.draw_button.pack(fill="x")

    def _create_visualization_area(self):
        viz_frame = ttk.Frame(self.master, style='TFrame')
        viz_frame.pack(pady=(10, 5), padx=20, fill="both", expand=True)
        
        viz_label = ttk.Label(viz_frame, text="📊 Visualização da Grade", 
                             style='Outer.TLabel', font=self.labelframe_font)
        viz_label.pack(pady=(0, 10))

        self.canvas_outer_frame = ttk.Frame(viz_frame, style='CanvasOuter.TFrame', padding=15)
        self.canvas_outer_frame.pack(fill="both", expand=True)

        self._create_canvas_widget()

    def _create_canvas_widget(self):
        self.canvas = tk.Canvas(self.canvas_outer_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
                               bg=CANVAS_BG_COLOR, highlightthickness=2, 
                               highlightbackground=AXIS_COLOR, relief="solid")
        self.canvas.pack(anchor="center")

    def _create_information_footer(self):
        info_text = (f"💡 Grade: [{WORLD_X_MIN},{WORLD_X_MAX_EDGE-1}] × [{WORLD_Y_MIN},{WORLD_Y_MAX_EDGE-1}] "
                    f"| 🔵 Pixels DDA | 🔴 Linha Ideal")
        
        self.info_label = ttk.Label(self.master, style='Outer.TLabel', text=info_text,
                                   font=(self.primary_font[0], FONT_SIZE_NORMAL-1),
                                   justify="center")
        self.info_label.pack(pady=(5, 20), padx=20)

    def _world_to_canvas_cell_coords(self, wx, wy):
        cx0 = (wx - WORLD_X_MIN) * CELL_SIZE
        cy0 = CANVAS_HEIGHT - ((wy + 1) - WORLD_Y_MIN) * CELL_SIZE
        cx1 = ((wx + 1) - WORLD_X_MIN) * CELL_SIZE
        cy1 = CANVAS_HEIGHT - (wy - WORLD_Y_MIN) * CELL_SIZE
        return cx0, cy0, cx1, cy1

    def _world_to_canvas_line_endpoint_coords(self, wx, wy):
        cx = (wx + 0.5 - WORLD_X_MIN) * CELL_SIZE
        cy = CANVAS_HEIGHT - (wy + 0.5 - WORLD_Y_MIN) * CELL_SIZE
        return cx, cy

    def _draw_initial_grid(self):
        self._clear_canvas()
        self._draw_grid_structure()
        self._draw_coordinates()
        self._draw_axis_markings()

    def _clear_canvas(self):
        self.canvas.delete("all")

    def _draw_grid_structure(self):
        self._draw_vertical_grid_lines()
        self._draw_horizontal_grid_lines()

    def _draw_vertical_grid_lines(self):
        for i in range(UNITS_X + 1):
            x_pos = i * CELL_SIZE
            world_x = WORLD_X_MIN + i
            is_main_axis = (world_x == 0)
            
            line_color = AXIS_COLOR if is_main_axis else GRID_COLOR
            line_width = 2 if is_main_axis else 1
            
            self.canvas.create_line(x_pos, 0, x_pos, CANVAS_HEIGHT, 
                                   fill=line_color, width=line_width, tags="grid_structure")

    def _draw_horizontal_grid_lines(self):
        for i in range(UNITS_Y + 1):
            y_pos = i * CELL_SIZE
            world_y = WORLD_Y_MIN + (UNITS_Y - i)
            is_main_axis = (world_y == 0)
            
            line_color = AXIS_COLOR if is_main_axis else GRID_COLOR
            line_width = 2 if is_main_axis else 1
            
            self.canvas.create_line(0, y_pos, CANVAS_WIDTH, y_pos,
                                   fill=line_color, width=line_width, tags="grid_structure")

    def _draw_coordinates(self):
        for world_x in range(WORLD_X_MIN, WORLD_X_MAX_EDGE):
            for world_y in range(WORLD_Y_MIN, WORLD_Y_MAX_EDGE):
                self._draw_cell_coordinate(world_x, world_y)

    def _draw_cell_coordinate(self, wx, wy):
        cx0, cy0, cx1, cy1 = self._world_to_canvas_cell_coords(wx, wy)
        center_x, center_y = (cx0 + cx1) / 2, (cy0 + cy1) / 2
        
        is_axis_cell = (wx == 0 or wy == 0)
        text_color = CELL_NUMBER_AXIS_COLOR if is_axis_cell else CELL_NUMBER_COLOR
        
        self.canvas.create_text(center_x, center_y, text=f"({wx},{wy})",
                               fill=text_color, font=self.cell_number_font,
                               tags="coordinates")

    def _draw_axis_markings(self):
        self._draw_x_axis_labels()
        self._draw_y_axis_labels()

    def _draw_x_axis_labels(self):
        for i in range(UNITS_X + 1):
            x_pos = i * CELL_SIZE
            world_x = WORLD_X_MIN + i
            
            if self._should_show_axis_label(world_x):
                self.canvas.create_text(x_pos, CANVAS_HEIGHT + 8, text=str(world_x),
                                       anchor="n", fill=TEXT_COLOR_PRIMARY, 
                                       font=self.grid_label_font, tags="axis_labels")

    def _draw_y_axis_labels(self):
        for i in range(UNITS_Y + 1):
            y_pos = i * CELL_SIZE
            world_y = WORLD_Y_MIN + (UNITS_Y - i)
            
            if self._should_show_axis_label(world_y):
                self.canvas.create_text(-8, y_pos, text=str(world_y),
                                       anchor="e", fill=TEXT_COLOR_PRIMARY,
                                       font=self.grid_label_font, tags="axis_labels")

    def _should_show_axis_label(self, value):
        return value % 2 == 0 or value == 0

    def dda_algorithm(self, x0, y0, x1, y1):
        pixels = []
        dx, dy = x1 - x0, y1 - y0
        steps = max(abs(dx), abs(dy))

        if steps == 0:
            return [(round(x0), round(y0))]

        x_increment = dx / steps
        y_increment = dy / steps
        x, y = float(x0), float(y0)

        for _ in range(int(steps) + 1):
            pixels.append((round(x), round(y)))
            x += x_increment
            y += y_increment
        
        return pixels

    def _execute_dda_algorithm(self):
        coordinates = self._get_input_coordinates()
        if coordinates is None:
            return

        self._clear_previous_results()
        x0, y0, x1, y1 = coordinates
        
        dda_pixels = self.dda_algorithm(x0, y0, x1, y1)
        self._visualize_results(dda_pixels, x0, y0, x1, y1)

    def _get_input_coordinates(self):
        try:
            return [int(entry.get()) for entry in [self.x0_entry, self.y0_entry, 
                                                  self.x1_entry, self.y1_entry]]
        except ValueError:
            messagebox.showerror("❌ Entrada Inválida", 
                               "Insira apenas números inteiros válidos.", 
                               parent=self.master)
            return None

    def _clear_previous_results(self):
        self.canvas.delete("dda_results", "ideal_line")

    def _visualize_results(self, pixels, x0, y0, x1, y1):
        self._highlight_dda_pixels(pixels)
        self._draw_ideal_reference_line(x0, y0, x1, y1)

    def _highlight_dda_pixels(self, pixels):
        for wx, wy in pixels:
            if self._is_within_bounds(wx, wy):
                self._draw_highlighted_pixel(wx, wy)

    def _is_within_bounds(self, wx, wy):
        return (WORLD_X_MIN <= wx < WORLD_X_MAX_EDGE and 
                WORLD_Y_MIN <= wy < WORLD_Y_MAX_EDGE)

    def _draw_highlighted_pixel(self, wx, wy):
        cx0, cy0, cx1, cy1 = self._world_to_canvas_cell_coords(wx, wy)
        
        self.canvas.create_rectangle(cx0+2, cy0+2, cx1-2, cy1-2, 
                                   fill=PIXEL_COLOR_DDA, outline=PIXEL_COLOR_DDA,
                                   tags="dda_results")
        
        center_x, center_y = (cx0 + cx1) / 2, (cy0 + cy1) / 2
        self.canvas.create_text(center_x, center_y, text=f"({wx},{wy})",
                               fill="white", font=(self.cell_number_font[0], 
                               self.cell_number_font[1], "bold"),
                               tags="dda_results")

    def _draw_ideal_reference_line(self, x0, y0, x1, y1):
        start_x, start_y = self._world_to_canvas_line_endpoint_coords(x0, y0)
        end_x, end_y = self._world_to_canvas_line_endpoint_coords(x1, y1)
        
        self.canvas.create_line(start_x, start_y, end_x, end_y,
                               fill=IDEAL_LINE_COLOR, width=3, dash=(10, 5), 
                               tags="ideal_line")


if __name__ == '__main__':
    root = tk.Tk()
    app = DDAGraphicalTest(root)
    root.mainloop()