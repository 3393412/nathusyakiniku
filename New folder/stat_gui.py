import pygame
import random
import csv
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class StatViewer(tk.Toplevel):
    def __init__(self, master, csv_path: str):
        super().__init__(master)
        self.title("Stat Graph Viewer")
        self.geometry("860x660")

        try:
            self.df = pd.read_csv(csv_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV:\n{e}")
            self.destroy()
            return
        if self.df.empty or len(self.df.columns) < 2:
            messagebox.showerror("Error", "CSV must have at least two columns.")
            self.destroy()
            return
        self.metrics = {
            "mouse_total_distance / click": {
                "series": lambda d: d["mouse_total_distance"] / d["click"],
                "ylabel": "distance per click",
                "types": ["Box", "Bar"],
            },
            "click / time": {
                "series": lambda d: d["click"] / d["time"],
                "ylabel": "click per second",
                "types": ["Line", "Bar"],
            },
            "serve / score": {
                "x": "serve",
                "y": "score",
                "types": ["Bar", "Scatter"],
            },
            "mouse_total_distance / serve": {
                "series": lambda d: d["mouse_total_distance"] / d["serve"],
                "ylabel": "distance per serve",
                "types": ["Box", "Bar"],
            },
        }


        top_bar = tk.Frame(self)
        top_bar.pack(pady=6)


        tk.Label(top_bar, text="Metric:").pack(side=tk.LEFT, padx=(0, 4))
        self.metric_cmb = ttk.Combobox(
            top_bar,
            values=list(self.metrics.keys()),
            state="readonly",
            width=35,
        )
        self.metric_cmb.current(0)
        self.metric_cmb.pack(side=tk.LEFT, padx=(0, 12))
        self.metric_cmb.bind("<<ComboboxSelected>>", self._on_metric_change)


        tk.Label(top_bar, text="Chart:").pack(side=tk.LEFT, padx=(0, 4))
        self.chart_cmb = ttk.Combobox(
            top_bar,
            state="readonly",
            width=12,
        )
        self.chart_cmb.pack(side=tk.LEFT)

        self.fig, self.ax = plt.subplots(figsize=(7.2, 4.6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=4, pady=4)


        ttk.Button(self, text="Close", command=self.destroy).pack(pady=8)

        self._on_metric_change()


    def _on_metric_change(self, *_):
        metric = self.metric_cmb.get()
        types = self.metrics[metric]["types"]
        self.chart_cmb["values"] = types

        if self.chart_cmb.get() not in types:
            self.chart_cmb.current(0)
        self._plot()

    def _plot(self, *_):
        metric_key = self.metric_cmb.get()
        chart_type = self.chart_cmb.get() or self.metrics[metric_key]["types"][0]
        spec = self.metrics[metric_key]

        self.ax.clear()


        if "series" in spec:
            series = spec["series"](self.df)

            if chart_type == "Box":
                self.ax.boxplot(series, vert=True)
                self.ax.set_xticks([1])
                self.ax.set_xticklabels([spec["ylabel"]])
            elif chart_type == "Bar":
                self.ax.bar(range(len(series)), series)
                self.ax.set_xticks(range(len(series)))
                self.ax.set_xticklabels(range(1, len(series) + 1))
                self.ax.set_xlabel("Session")
            elif chart_type == "Line":
                self.ax.plot(range(len(series)), series, marker="o")
                self.ax.set_xlabel("Session")

            self.ax.set_ylabel(spec["ylabel"])
            self.ax.set_title(f"{spec['ylabel']}  —  {chart_type}")


        else:
            x, y = spec["x"], spec["y"]
            if chart_type == "Scatter":
                self.ax.scatter(self.df[x], self.df[y], marker="o")
            elif chart_type == "Bar":
                self.ax.bar(self.df[x], self.df[y])

            self.ax.set_xlabel(x)
            self.ax.set_ylabel(y)
            self.ax.set_title(f"{y} vs {x}  —  {chart_type}")

        self.ax.grid(True)
        self.fig.tight_layout()
        self.canvas.draw()


    def _on_chart_change(self, *_):
        self._plot()


    def __post_init__(self):
        self.chart_cmb.bind("<<ComboboxSelected>>", self._on_chart_change)