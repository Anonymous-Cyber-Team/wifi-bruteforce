"""
WiFi Password Wordlist Generator
Generates custom password wordlists for WiFi brute force testing.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import itertools
import os
import time
import string

# ─────────────────────────── Colors ─────────────────────────────────────────
BG_DARK      = "#0d1117"
BG_CARD      = "#161b22"
BG_CARD2     = "#1c2128"
ACCENT       = "#58a6ff"
ACCENT_GREEN = "#3fb950"
ACCENT_RED   = "#f85149"
ACCENT_ORANGE= "#e3b341"
ACCENT_PURPLE= "#bc8cff"
TEXT_PRIMARY = "#e6edf3"
TEXT_MUTED   = "#8b949e"
BORDER       = "#30363d"
BUTTON_BG    = "#21262d"

FONT_TITLE  = ("Segoe UI", 18, "bold")
FONT_SUB    = ("Segoe UI", 11, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_MONO   = ("Consolas", 9)


# ─────────────────────────── Generator Logic ─────────────────────────────────
class WordlistGenerator:
    def generate_combination(self, charset, min_len, max_len, output_path,
                              on_progress, on_done):
        """Generate all combinations of charset between min/max length."""
        count = 0
        estimated = sum(len(charset) ** l for l in range(min_len, max_len + 1))
        start = time.time()

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                for length in range(min_len, max_len + 1):
                    for combo in itertools.product(charset, repeat=length):
                        password = "".join(combo)
                        f.write(password + "\n")
                        count += 1

                        if count % 10000 == 0:
                            elapsed = time.time() - start
                            speed = count / elapsed if elapsed > 0 else 0
                            pct = min((count / estimated * 100), 99.9)
                            on_progress(count, estimated, speed, pct)

            on_done(count, output_path, True)
        except Exception as e:
            on_done(0, str(e), False)

    def generate_wordlist_from_keywords(self, keywords, years, symbols,
                                         leetspeak, output_path, on_progress, on_done):
        """Generate smart wordlist from keywords with variations."""
        passwords = set()
        leet_map = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7"}

        for kw in keywords:
            kw = kw.strip()
            if not kw:
                continue

            variants = {kw, kw.lower(), kw.upper(), kw.capitalize()}

            if leetspeak:
                leet_ver = kw.lower()
                for ch, rep in leet_map.items():
                    leet_ver = leet_ver.replace(ch, rep)
                variants.add(leet_ver)

            for var in list(variants):
                passwords.add(var)
                # Add numbers
                for n in ["1", "12", "123", "1234", "12345", "123456"]:
                    passwords.add(var + n)
                    passwords.add(n + var)
                # Add years
                for y in years:
                    passwords.add(var + y)
                    passwords.add(y + var)
                # Add symbols
                for sym in symbols:
                    passwords.add(var + sym)
                    passwords.add(sym + var)
                # Combined
                for y in years:
                    for sym in symbols:
                        passwords.add(var + y + sym)
                        passwords.add(sym + var + y)

        count = 0
        total = len(passwords)

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                for pw in sorted(passwords, key=len):
                    f.write(pw + "\n")
                    count += 1
                    if count % 100 == 0:
                        on_progress(count, total, 0, count / total * 100)

            on_done(count, output_path, True)
        except Exception as e:
            on_done(0, str(e), False)

    def merge_wordlists(self, file_paths, output_path, deduplicate, on_done):
        """Merge multiple wordlists into one."""
        seen = set()
        count = 0
        try:
            with open(output_path, "w", encoding="utf-8") as out:
                for path in file_paths:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            pw = line.strip()
                            if not pw:
                                continue
                            if deduplicate:
                                if pw in seen:
                                    continue
                                seen.add(pw)
                            out.write(pw + "\n")
                            count += 1
            on_done(count, output_path, True)
        except Exception as e:
            on_done(0, str(e), False)


# ─────────────────────────── GUI ─────────────────────────────────────────────
class WordlistGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.generator = WordlistGenerator()
        self.generating = False
        self.merge_files = []

        self._setup_window()
        self._build_ui()

    def _setup_window(self):
        self.root.title("Wordlist Generator — WiFi Bruteforcer Suite")
        self.root.geometry("860x680")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(True, True)

        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 860) // 2
        y = (self.root.winfo_screenheight() - 680) // 2
        self.root.geometry(f"860x680+{x}+{y}")

    def _build_ui(self):
        # ── Header ──
        header = tk.Frame(self.root, bg=BG_CARD, pady=14)
        header.pack(fill="x")

        tk.Label(header, text="🔐  Wordlist Generator",
                 font=FONT_TITLE, bg=BG_CARD, fg=ACCENT_PURPLE).pack()
        tk.Label(header, text="WiFi Password Dictionary Creator",
                 font=FONT_BODY, bg=BG_CARD, fg=TEXT_MUTED).pack()

        # ── Tabs ──
        tab_frame = tk.Frame(self.root, bg=BG_DARK, pady=10)
        tab_frame.pack(fill="x", padx=20)

        self.tab_buttons = {}
        self.current_tab = tk.StringVar(value="smart")
        tabs = [
            ("smart",  "🧠  Smart Generator"),
            ("brute",  "⚡  Brute Force"),
            ("merge",  "🔗  Merge Lists"),
        ]

        for tab_id, tab_name in tabs:
            btn = tk.Button(
                tab_frame, text=tab_name, font=FONT_BODY,
                bg=ACCENT if tab_id == "smart" else BUTTON_BG,
                fg=BG_DARK if tab_id == "smart" else TEXT_MUTED,
                relief="flat", bd=0, padx=14, pady=6, cursor="hand2",
                command=lambda t=tab_id: self._switch_tab(t)
            )
            btn.pack(side="left", padx=4)
            self.tab_buttons[tab_id] = btn

        # ── Content Area ──
        self.content_frame = tk.Frame(self.root, bg=BG_DARK)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.frames = {}
        self.frames["smart"] = self._build_smart_tab(self.content_frame)
        self.frames["brute"] = self._build_brute_tab(self.content_frame)
        self.frames["merge"] = self._build_merge_tab(self.content_frame)

        self._switch_tab("smart")

        # ── Progress Bar ──
        prog_card = tk.Frame(self.root, bg=BG_CARD, pady=8, padx=14,
                             highlightbackground=BORDER, highlightthickness=1)
        prog_card.pack(fill="x", padx=20, pady=(0, 10))

        prog_row = tk.Frame(prog_card, bg=BG_CARD)
        prog_row.pack(fill="x")

        self.prog_lbl = tk.Label(prog_row, text="Ready", font=FONT_BODY,
                                  bg=BG_CARD, fg=TEXT_MUTED)
        self.prog_lbl.pack(side="left")

        self.count_lbl = tk.Label(prog_row, text="", font=FONT_MONO,
                                   bg=BG_CARD, fg=ACCENT)
        self.count_lbl.pack(side="right")

        style = ttk.Style()
        style.configure("Gen.Horizontal.TProgressbar",
                         troughcolor=BG_CARD2, background=ACCENT_PURPLE,
                         thickness=14, borderwidth=0)
        self.progress = ttk.Progressbar(prog_card,
                                         style="Gen.Horizontal.TProgressbar",
                                         mode="determinate")
        self.progress.pack(fill="x", pady=(4, 0))

    # ── Tab Builder ───────────────────────────────────────────────────────────
    def _build_smart_tab(self, parent):
        frame = tk.Frame(parent, bg=BG_DARK)

        # Keywords
        kw_card = tk.Frame(frame, bg=BG_CARD, pady=10, padx=14,
                           highlightbackground=BORDER, highlightthickness=1)
        kw_card.pack(fill="x", pady=(0, 8))

        tk.Label(kw_card, text="🔤  Keywords (one per line)",
                 font=FONT_SUB, bg=BG_CARD, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Label(kw_card, text="Enter names, words, pet names, places, etc.",
                 font=FONT_BODY, bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")
        tk.Frame(kw_card, bg=BORDER, height=1).pack(fill="x", pady=6)

        self.keywords_text = tk.Text(
            kw_card, height=5, bg=BG_CARD2, fg=TEXT_PRIMARY,
            font=FONT_MONO, relief="flat", bd=6,
            insertbackground=ACCENT
        )
        self.keywords_text.pack(fill="x")
        self.keywords_text.insert("1.0", "admin\nrouter\nhome\nwifi\n")

        # Options Row
        opt_row = tk.Frame(frame, bg=BG_DARK)
        opt_row.pack(fill="x", pady=(0, 8))

        # Years
        yr_card = tk.Frame(opt_row, bg=BG_CARD, pady=10, padx=14,
                           highlightbackground=BORDER, highlightthickness=1)
        yr_card.pack(side="left", fill="both", expand=True, padx=(0, 6))

        tk.Label(yr_card, text="📅  Years", font=FONT_SUB,
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Frame(yr_card, bg=BORDER, height=1).pack(fill="x", pady=4)

        self.years_text = tk.Text(yr_card, height=3, bg=BG_CARD2,
                                   fg=TEXT_PRIMARY, font=FONT_MONO,
                                   relief="flat", bd=4, insertbackground=ACCENT)
        self.years_text.pack(fill="x")
        self.years_text.insert("1.0", "2019\n2020\n2021\n2022\n2023\n2024\n2025")

        # Symbols & Options
        sym_card = tk.Frame(opt_row, bg=BG_CARD, pady=10, padx=14,
                            highlightbackground=BORDER, highlightthickness=1)
        sym_card.pack(side="left", fill="both", expand=True)

        tk.Label(sym_card, text="⚙️  Options", font=FONT_SUB,
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Frame(sym_card, bg=BORDER, height=1).pack(fill="x", pady=4)

        tk.Label(sym_card, text="Symbols:", font=FONT_BODY,
                 bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")

        self.symbols_var = tk.StringVar(value="!@#$")
        sym_entry = tk.Entry(sym_card, textvariable=self.symbols_var,
                              bg=BG_CARD2, fg=TEXT_PRIMARY, font=FONT_MONO,
                              relief="flat", bd=4, insertbackground=ACCENT)
        sym_entry.pack(fill="x", pady=(2, 6))

        self.leet_var = tk.BooleanVar(value=True)
        tk.Checkbutton(sym_card, text="Leetspeak (e→3, a→4, etc.)",
                       variable=self.leet_var, font=FONT_BODY,
                       bg=BG_CARD, fg=TEXT_PRIMARY, selectcolor=BG_CARD2,
                       activebackground=BG_CARD).pack(anchor="w")

        # Output & Generate
        self._build_output_generate(frame, self._generate_smart)

        return frame

    def _build_brute_tab(self, parent):
        frame = tk.Frame(parent, bg=BG_DARK)

        # Charset selection
        cs_card = tk.Frame(frame, bg=BG_CARD, pady=10, padx=14,
                           highlightbackground=BORDER, highlightthickness=1)
        cs_card.pack(fill="x", pady=(0, 8))

        tk.Label(cs_card, text="🔡  Character Set", font=FONT_SUB,
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Frame(cs_card, bg=BORDER, height=1).pack(fill="x", pady=6)

        check_row = tk.Frame(cs_card, bg=BG_CARD)
        check_row.pack(fill="x")

        self.cs_lower = tk.BooleanVar(value=True)
        self.cs_upper = tk.BooleanVar(value=False)
        self.cs_digits = tk.BooleanVar(value=True)
        self.cs_symbols = tk.BooleanVar(value=False)

        for text, var in [
            ("a-z lowercase", self.cs_lower),
            ("A-Z uppercase", self.cs_upper),
            ("0-9 digits",    self.cs_digits),
            ("Symbols !@#$",  self.cs_symbols),
        ]:
            tk.Checkbutton(
                check_row, text=text, variable=var, font=FONT_BODY,
                bg=BG_CARD, fg=TEXT_PRIMARY, selectcolor=BG_CARD2,
                activebackground=BG_CARD
            ).pack(side="left", padx=10)

        # Custom charset
        tk.Label(cs_card, text="Custom charset (leave empty to use above):",
                 font=FONT_BODY, bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w", pady=(8, 2))
        self.custom_charset = tk.StringVar()
        tk.Entry(cs_card, textvariable=self.custom_charset,
                 bg=BG_CARD2, fg=TEXT_PRIMARY, font=FONT_MONO,
                 relief="flat", bd=4, insertbackground=ACCENT).pack(fill="x")

        # Length
        len_card = tk.Frame(frame, bg=BG_CARD, pady=10, padx=14,
                            highlightbackground=BORDER, highlightthickness=1)
        len_card.pack(fill="x", pady=(0, 8))

        tk.Label(len_card, text="📏  Password Length", font=FONT_SUB,
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Frame(len_card, bg=BORDER, height=1).pack(fill="x", pady=6)

        len_row = tk.Frame(len_card, bg=BG_CARD)
        len_row.pack()

        tk.Label(len_row, text="Min:", font=FONT_BODY,
                 bg=BG_CARD, fg=TEXT_MUTED).pack(side="left")
        self.min_len = tk.Spinbox(len_row, from_=1, to=12, width=4, font=FONT_BODY,
                                   bg=BG_CARD2, fg=TEXT_PRIMARY, relief="flat",
                                   buttonbackground=BG_CARD2)
        self.min_len.delete(0, "end")
        self.min_len.insert(0, "6")
        self.min_len.pack(side="left", padx=6)

        tk.Label(len_row, text="Max:", font=FONT_BODY,
                 bg=BG_CARD, fg=TEXT_MUTED).pack(side="left", padx=(12, 0))
        self.max_len = tk.Spinbox(len_row, from_=1, to=12, width=4, font=FONT_BODY,
                                   bg=BG_CARD2, fg=TEXT_PRIMARY, relief="flat",
                                   buttonbackground=BG_CARD2)
        self.max_len.delete(0, "end")
        self.max_len.insert(0, "8")
        self.max_len.pack(side="left", padx=6)

        # Warning
        tk.Label(len_card, text="⚠ Warning: Large charsets + long lengths = very large files!",
                 font=FONT_BODY, bg=BG_CARD, fg=ACCENT_ORANGE).pack(anchor="w", pady=(6, 0))

        self._build_output_generate(frame, self._generate_brute)

        return frame

    def _build_merge_tab(self, parent):
        frame = tk.Frame(parent, bg=BG_DARK)

        # File list
        list_card = tk.Frame(frame, bg=BG_CARD, pady=10, padx=14,
                             highlightbackground=BORDER, highlightthickness=1)
        list_card.pack(fill="both", expand=True, pady=(0, 8))

        hdr = tk.Frame(list_card, bg=BG_CARD)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📂  Wordlist Files to Merge", font=FONT_SUB,
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(side="left")

        btn_row = tk.Frame(list_card, bg=BG_CARD)
        btn_row.pack(fill="x", pady=6)

        add_btn = tk.Button(btn_row, text="+ Add Files", font=FONT_BODY,
                             bg=BUTTON_BG, fg=ACCENT, relief="flat", bd=0,
                             padx=10, pady=4, cursor="hand2",
                             command=self._add_merge_files)
        add_btn.pack(side="left", padx=(0, 6))

        clr_btn = tk.Button(btn_row, text="Clear All", font=FONT_BODY,
                             bg=BUTTON_BG, fg=ACCENT_RED, relief="flat", bd=0,
                             padx=10, pady=4, cursor="hand2",
                             command=self._clear_merge_files)
        clr_btn.pack(side="left")

        tk.Frame(list_card, bg=BORDER, height=1).pack(fill="x")

        self.merge_listbox = tk.Listbox(
            list_card, bg=BG_CARD2, fg=TEXT_PRIMARY, font=FONT_MONO,
            relief="flat", bd=6, height=8, selectbackground=ACCENT,
            selectforeground=BG_DARK
        )
        self.merge_listbox.pack(fill="both", expand=True, pady=4)

        # Options
        opt_card = tk.Frame(frame, bg=BG_CARD, pady=10, padx=14,
                            highlightbackground=BORDER, highlightthickness=1)
        opt_card.pack(fill="x", pady=(0, 8))

        self.dedup_var = tk.BooleanVar(value=True)
        tk.Checkbutton(opt_card, text="Remove duplicate passwords",
                       variable=self.dedup_var, font=FONT_BODY,
                       bg=BG_CARD, fg=TEXT_PRIMARY, selectcolor=BG_CARD2,
                       activebackground=BG_CARD).pack(anchor="w")

        self._build_output_generate(frame, self._generate_merge)

        return frame

    def _build_output_generate(self, parent, command):
        """Shared output path + generate button."""
        out_card = tk.Frame(parent, bg=BG_CARD, pady=10, padx=14,
                            highlightbackground=BORDER, highlightthickness=1)
        out_card.pack(fill="x", pady=(0, 8))

        hdr = tk.Frame(out_card, bg=BG_CARD)
        hdr.pack(fill="x")
        tk.Label(hdr, text="💾  Save Output To:", font=FONT_BODY,
                 bg=BG_CARD, fg=TEXT_MUTED).pack(side="left")

        out_row = tk.Frame(out_card, bg=BG_CARD2,
                           highlightbackground=BORDER, highlightthickness=1)
        out_row.pack(fill="x", pady=6)

        out_var = tk.StringVar(value=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"custom_wordlist_{int(time.time())}.txt"
        ))
        setattr(self, f"out_var_{command.__name__}", out_var)

        tk.Entry(out_row, textvariable=out_var, bg=BG_CARD2, fg=TEXT_PRIMARY,
                 font=FONT_MONO, relief="flat", bd=6,
                 insertbackground=ACCENT).pack(side="left", fill="x", expand=True)

        tk.Button(out_row, text="📁", font=FONT_BODY, bg=BG_CARD2,
                  fg=TEXT_MUTED, relief="flat", bd=0, padx=6, cursor="hand2",
                  command=lambda v=out_var: self._browse_output(v)
                  ).pack(side="right")

        gen_btn = tk.Button(
            out_card, text=f"⚡  Generate Wordlist", font=("Segoe UI", 11, "bold"),
            bg=ACCENT_PURPLE, fg="white", relief="flat", bd=0,
            padx=12, pady=8, cursor="hand2",
            command=lambda v=out_var: command(v.get())
        )
        gen_btn.pack(fill="x")

    # ── Tab Switch ────────────────────────────────────────────────────────────
    def _switch_tab(self, tab_id):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[tab_id].pack(fill="both", expand=True)
        self.current_tab.set(tab_id)

        for tid, btn in self.tab_buttons.items():
            if tid == tab_id:
                btn.config(bg=ACCENT, fg=BG_DARK)
            else:
                btn.config(bg=BUTTON_BG, fg=TEXT_MUTED)

    # ── Actions ───────────────────────────────────────────────────────────────
    def _browse_output(self, var):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            var.set(path)

    def _add_merge_files(self):
        paths = filedialog.askopenfilenames(
            title="Select Wordlist Files",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        for p in paths:
            if p not in self.merge_files:
                self.merge_files.append(p)
                self.merge_listbox.insert("end", f"  {p}")

    def _clear_merge_files(self):
        self.merge_files.clear()
        self.merge_listbox.delete(0, "end")

    def _on_progress(self, current, total, speed, pct):
        def update():
            self.progress["value"] = min(pct, 99.9)
            self.prog_lbl.config(text=f"Generating... {pct:.1f}%", fg=ACCENT_PURPLE)
            self.count_lbl.config(text=f"{current:,} passwords")
        self.root.after(0, update)

    def _on_done(self, count, path, success):
        def update():
            self.generating = False
            self.progress["value"] = 100 if success else 0
            if success:
                self.prog_lbl.config(text=f"✅ Done!", fg=ACCENT_GREEN)
                self.count_lbl.config(text=f"{count:,} passwords generated")
                messagebox.showinfo(
                    "Done!",
                    f"✅ Wordlist generated!\n\n"
                    f"Passwords: {count:,}\n"
                    f"Saved to: {path}"
                )
            else:
                self.prog_lbl.config(text=f"❌ Error: {path}", fg=ACCENT_RED)
        self.root.after(0, update)

    def _generate_smart(self, out_path):
        if self.generating:
            return
        keywords = self.keywords_text.get("1.0", "end").strip().splitlines()
        years = self.years_text.get("1.0", "end").strip().splitlines()
        symbols = list(self.symbols_var.get())
        leet = self.leet_var.get()

        if not keywords:
            messagebox.showwarning("No Keywords", "Enter at least one keyword!")
            return

        self.generating = True
        self.prog_lbl.config(text="Generating...", fg=ACCENT_PURPLE)
        self.progress["value"] = 0

        threading.Thread(
            target=self.generator.generate_wordlist_from_keywords,
            args=(keywords, years, symbols, leet, out_path,
                  self._on_progress, self._on_done),
            daemon=True
        ).start()

    def _generate_brute(self, out_path):
        if self.generating:
            return

        custom = self.custom_charset.get().strip()
        if custom:
            charset = custom
        else:
            charset = ""
            if self.cs_lower.get(): charset += string.ascii_lowercase
            if self.cs_upper.get(): charset += string.ascii_uppercase
            if self.cs_digits.get(): charset += string.digits
            if self.cs_symbols.get(): charset += "!@#$%^&*"

        if not charset:
            messagebox.showwarning("No Charset", "Select at least one character set!")
            return

        try:
            min_l = int(self.min_len.get())
            max_l = int(self.max_len.get())
        except ValueError:
            min_l, max_l = 6, 8

        # Estimate size
        estimated = sum(len(charset) ** l for l in range(min_l, max_l + 1))
        if estimated > 50_000_000:
            ans = messagebox.askyesno(
                "Large File Warning",
                f"Estimated passwords: {estimated:,}\n"
                f"This could be a very large file and take a long time.\n\n"
                f"Continue anyway?"
            )
            if not ans:
                return

        self.generating = True
        self.prog_lbl.config(text="Generating...", fg=ACCENT_PURPLE)
        self.progress["value"] = 0

        threading.Thread(
            target=self.generator.generate_combination,
            args=(charset, min_l, max_l, out_path,
                  self._on_progress, self._on_done),
            daemon=True
        ).start()

    def _generate_merge(self, out_path):
        if self.generating or not self.merge_files:
            if not self.merge_files:
                messagebox.showwarning("No Files", "Add at least one wordlist file!")
            return

        self.generating = True
        dedup = self.dedup_var.get()

        threading.Thread(
            target=self.generator.merge_wordlists,
            args=(self.merge_files, out_path, dedup, self._on_done),
            daemon=True
        ).start()


# ─────────────────────────── Entry Point ─────────────────────────────────────
def main():
    root = tk.Tk()
    app = WordlistGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
