import tkinter as tk
from tkinter import ttk
import tomasulo

t = tomasulo
toma = t.Tomasulo()
toma.simulador()

index = 0

# Paleta de Cores (Tema Claro - Tons Terrosos)
COLORS = {
    "bg_window": "#FAF9F6",     # Off-White
    "text": "#291C0E",          # Cafe Escuro
    "header_bg": "#DCC8B8",     # Bege Medio
    "header_text": "#291C0E",   # Texto Escuro
    "row_even": "#FFFFFF",      # Branco
    "row_odd": "#F2EBE5",       # Bege Claro
    "sash": "#BCAAA4",          # Divisor
    "select": "#A78D78",        # Selecao
    "border": "#8D6E63"         # Borda Fina
}

def setup_style():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(".", background=COLORS["bg_window"], foreground=COLORS["text"], font=("Segoe UI", 10))

    style.configure("Treeview", 
        background=COLORS["row_even"], 
        fieldbackground=COLORS["row_even"], 
        foreground=COLORS["text"], 
        rowheight=28, 
        borderwidth=0
    )
    
    style.configure("Treeview.Heading", 
        background=COLORS["header_bg"], 
        foreground=COLORS["header_text"], 
        relief="flat", 
        font=("Segoe UI", 10, "bold")
    )
    style.map("Treeview.Heading", background=[("active", COLORS["select"])])

    style.configure("TButton", 
        background=COLORS["header_bg"], 
        foreground=COLORS["header_text"], 
        font=("Segoe UI", 10, "bold"), 
        padding=6, 
        borderwidth=1,
        bordercolor=COLORS["border"]
    )
    style.map("TButton", background=[("active", COLORS["select"])])

    style.configure("TLabelframe", background=COLORS["bg_window"], borderwidth=1, relief="solid", bordercolor=COLORS["sash"])
    style.configure("TLabelframe.Label", background=COLORS["bg_window"], foreground=COLORS["text"], font=("Segoe UI", 11, "bold"))
    
    style.configure("TPanedwindow", background=COLORS["bg_window"])
    style.configure("Sash", sashthickness=4, sashrelief="flat", background=COLORS["sash"]) 

    style.configure("Vertical.TScrollbar", troughcolor=COLORS["bg_window"], background=COLORS["sash"], borderwidth=0)
    style.configure("Horizontal.TScrollbar", troughcolor=COLORS["bg_window"], background=COLORS["sash"], borderwidth=0)

def create_responsive_table(parent, columns, height=5):
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True) 
    
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    v_scroll = ttk.Scrollbar(frame, orient="vertical")
    h_scroll = ttk.Scrollbar(frame, orient="horizontal")

    table = ttk.Treeview(frame, columns=columns, show="headings", height=height,
                         yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    
    v_scroll.config(command=table.yview)
    h_scroll.config(command=table.xview)

    table.grid(row=0, column=0, sticky="nsew")
    v_scroll.grid(row=0, column=1, sticky="ns")
    h_scroll.grid(row=1, column=0, sticky="ew")

    for col in columns:
        col_width = max(80, len(col) * 11)
        table.heading(col, text=col)
        table.column(col, width=col_width, minwidth=60, anchor="center", stretch=True)

    return table

def update_table_data(table, matrix):
    for item in table.get_children():
        table.delete(item)
    if not matrix: return
    for i, row in enumerate(matrix[1:]):
        tag = "even" if i % 2 == 0 else "odd"
        table.insert("", "end", values=row, tags=(tag,))
    
    table.tag_configure("even", background=COLORS["row_even"])
    table.tag_configure("odd", background=COLORS["row_odd"])

def update_interface():
    global index
    
    raw_ipc = toma.IIpc[index] if index < len(toma.IIpc) else 0.0
    try:
        ipc_formatted = f"{float(raw_ipc):.3f}"
    except (ValueError, TypeError):
        ipc_formatted = str(raw_ipc)

    # Logica original: Se for o primeiro clock, mostra 0 fixo
    if index == 0:
        bolhas_val = 0
    else:
        bolhas_val = toma.bobolhas[index] if index < len(toma.bobolhas) else "-"
    
    lbl_clock_val.config(text=str(index))
    lbl_ipc_val.config(text=ipc_formatted)
    lbl_bolha_val.config(text=str(bolhas_val))

    try:
        update_table_data(tbl_status, toma.status_das_instrucoes[index])
        update_table_data(tbl_rob, toma.buff[index])
        update_table_data(tbl_uf, toma.UniFunc[index])
        update_table_data(tbl_reg, toma.regregis[index])
    except IndexError:
        pass

def navegar(direcao):
    global index
    max_len = len(toma.geral) - 1
    novo_index = index + direcao
    
    if 0 <= novo_index <= max_len:
        index = novo_index
        update_interface()
        
        # Estado dos botoes
        if index == 0:
            btn_prev.state(["disabled"])
        else:
            btn_prev.state(["!disabled"])
            
        if index == max_len:
            btn_next.state(["disabled"])
        else:
            btn_next.state(["!disabled"])

root = tk.Tk()
root.title("Simulador Tomasulo")
root.geometry("1200x800")
root.configure(bg=COLORS["bg_window"])

setup_style()

# Header e Controles
header_frame = tk.Frame(root, bg=COLORS["bg_window"])
header_frame.pack(fill="x", padx=15, pady=10)

nav_frame = tk.Frame(header_frame, bg=COLORS["bg_window"])
nav_frame.pack(side="left")
btn_prev = ttk.Button(nav_frame, text="< Voltar", command=lambda: navegar(-1))
btn_prev.pack(side="left", padx=(0, 10))
btn_next = ttk.Button(nav_frame, text="Avancar >", command=lambda: navegar(1))
btn_next.pack(side="left")

metrics_frame = tk.Frame(header_frame, bg=COLORS["bg_window"])
metrics_frame.pack(side="right")

def create_metric(parent, label, initial):
    f = tk.Frame(parent, bg=COLORS["bg_window"])
    f.pack(side="left", padx=15)
    tk.Label(f, text=label, font=("Segoe UI", 9, "bold"), bg=COLORS["bg_window"], fg=COLORS["text"]).pack(anchor="w")
    l_val = tk.Label(f, text=initial, font=("Consolas", 14), bg=COLORS["bg_window"], fg=COLORS["text"])
    l_val.pack(anchor="w")
    return l_val

lbl_clock_val = create_metric(metrics_frame, "CLOCK", "0")
lbl_ipc_val = create_metric(metrics_frame, "IPC", "0.000")
lbl_bolha_val = create_metric(metrics_frame, "BOLHAS", "0")

# Layout de Paineis
main_pane = ttk.PanedWindow(root, orient="vertical")
main_pane.pack(fill="both", expand=True, padx=10, pady=5)

top_pane = ttk.PanedWindow(main_pane, orient="horizontal")
main_pane.add(top_pane, weight=2)

bottom_pane = ttk.PanedWindow(main_pane, orient="horizontal")
main_pane.add(bottom_pane, weight=1)

# Areas das Tabelas
frame_status = ttk.LabelFrame(top_pane, text="Status das Instrucoes")
top_pane.add(frame_status, weight=1)
tbl_status = create_responsive_table(frame_status, toma.status_das_instrucoes[0][0])

frame_rob = ttk.LabelFrame(top_pane, text="Buffer de Reordenamento (ROB)")
top_pane.add(frame_rob, weight=1)
tbl_rob = create_responsive_table(frame_rob, toma.buff[0][0])

frame_uf = ttk.LabelFrame(bottom_pane, text="Unidades Funcionais (RS)")
bottom_pane.add(frame_uf, weight=1)
tbl_uf = create_responsive_table(frame_uf, toma.UniFunc[0][0])

frame_reg = ttk.LabelFrame(bottom_pane, text="Estado dos Registradores")
bottom_pane.add(frame_reg, weight=1)
tbl_reg = create_responsive_table(frame_reg, toma.regregis[0][0])

# Atalhos de Teclado
root.bind('<Left>', lambda e: navegar(-1))
root.bind('<Right>', lambda e: navegar(1))

update_interface()
root.mainloop()