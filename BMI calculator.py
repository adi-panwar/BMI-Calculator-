import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("PANFAR BMI Calculator")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        
        self.data_file = "bmi_data.json"
        self.users_data = self.load_data()
        
        self.bg_color = "#b6f3b4"
        self.primary_color = "#D01212"
        self.secondary_color = "#E161B2"
        
        self.root.configure(bg=self.bg_color)
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10 )
        
        self.calculator_tab = ttk.Frame(self.notebook)
        self.history_tab = ttk.Frame(self.notebook)
        self.statistics_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.calculator_tab, text="BMI Calculator")
        self.notebook.add(self.history_tab, text="History")
        self.notebook.add(self.statistics_tab, text="Statistics & Trends")
        
        self.setup_calculator_tab()
        self.setup_history_tab()
        self.setup_statistics_tab()
        
    def load_data(self):
        """Load user data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_data(self):
        """Save user data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.users_data, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
            return False
    
    def calculate_bmi(self, weight, height):
        """Calculate BMI from weight (kg) and height (cm)"""
        height_m = height / 100
        return weight / (height_m ** 2)
    
    def categorize_bmi(self, bmi):
        """Categorize BMI value"""
        if bmi < 18.5:
            return "Underweight", "#3498db"
        elif 18.5 <= bmi < 25:
            return "Normal weight", "#193ab1"
        elif 25 <= bmi < 30:
            return "Overweight", "#f39c12"
        else:
            return "Obese", "#e74c3c"
    
    def setup_calculator_tab(self):
        """Setup the BMI calculator interface"""
        
        main_frame = tk.Frame(self.calculator_tab, bg=self.bg_color)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
       
        title = tk.Label(main_frame, text="PANFAR's BMI Calculator", 
                        font=("Arial", 24, "bold"), bg=self.bg_color, fg="#333")
        title.pack(pady=10)
        
        
        input_frame = tk.LabelFrame(main_frame, text="User Information", 
                                   font=("Arial", 12, "bold"), bg=self.bg_color, 
                                   padx=20, pady=20)
        input_frame.pack(pady=10, fill='x')
        
        tk.Label(input_frame, text="Username:", font=("Arial", 11), 
                bg=self.bg_color).grid(row=0, column=0, sticky='w', pady=5)
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(input_frame, textvariable=self.username_var, 
                                   font=("Arial", 11), width=25)
        username_entry.grid(row=0, column=1, padx=10, pady=5)
        
        
        tk.Label(input_frame, text="Weight (kg):", font=("Arial", 11), 
                bg=self.bg_color).grid(row=1, column=0, sticky='w', pady=5)
        self.weight_var = tk.StringVar()
        weight_entry = ttk.Entry(input_frame, textvariable=self.weight_var, 
                                font=("Arial", 11), width=25)
        weight_entry.grid(row=1, column=1, padx=10, pady=5)
        
        
        tk.Label(input_frame, text="Height (cm):", font=("Arial", 11), 
                bg=self.bg_color).grid(row=2, column=0, sticky='w', pady=5)
        self.height_var = tk.StringVar()
        height_entry = ttk.Entry(input_frame, textvariable=self.height_var, 
                                font=("Arial", 11), width=25)
        height_entry.grid(row=2, column=1, padx=10, pady=5)
        
        
        calc_btn = tk.Button(main_frame, text="Calculate BMI", 
                            command=self.calculate_and_save,
                            font=("Arial", 12, "bold"), bg=self.primary_color, 
                            fg="white", padx=20, pady=10, cursor="hand2")
        calc_btn.pack(pady=15)
        
       
        self.result_frame = tk.LabelFrame(main_frame, text="Results", 
                                         font=("Arial", 12, "bold"), 
                                         bg=self.bg_color, padx=20, pady=20)
        self.result_frame.pack(pady=10, fill='both', expand=True)
        
        self.result_label = tk.Label(self.result_frame, text="", 
                                     font=("Arial", 14), bg=self.bg_color, 
                                     wraplength=600)
        self.result_label.pack()
        
       
        ref_frame = tk.LabelFrame(main_frame, text="BMI Reference", 
                                 font=("Arial", 10, "bold"), bg=self.bg_color)
        ref_frame.pack(pady=5, fill='x')
        
        references = [
            ("Underweight", "< 18.5", "#3498db"),
            ("Normal", "18.5 - 24.9", "#2ecc71"),
            ("Overweight", "25 - 29.9", "#f39c12"),
            ("Obese", "≥ 30", "#e74c3c")
        ]
        
        for i, (cat, range_val, color) in enumerate(references):
            frame = tk.Frame(ref_frame, bg=self.bg_color)
            frame.pack(side='left', expand=True, padx=5, pady=5)
            tk.Label(frame, text="●", fg=color, font=("Arial", 16), 
                    bg=self.bg_color).pack(side='left')
            tk.Label(frame, text=f"{cat}: {range_val}", font=("Arial", 9), 
                    bg=self.bg_color).pack(side='left', padx=5)
    
    def validate_input(self, username, weight, height):
        """Validate user inputs"""
        if not username.strip():
            messagebox.showerror("Error", "Please enter a username")
            return False
        
        try:
            weight = float(weight)
            if weight <= 0 or weight > 500:
                messagebox.showerror("Error", "Weight must be between 0 and 500 kg")
                return False
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid weight")
            return False
        
        try:
            height = float(height)
            if height <= 0 or height > 300:
                messagebox.showerror("Error", "Height must be between 0 and 300 cm")
                return False
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid height")
            return False
        
        return True
    
    def calculate_and_save(self):
        """Calculate BMI and save to history"""
        username = self.username_var.get()
        weight = self.weight_var.get()
        height = self.height_var.get()
        
        if not self.validate_input(username, weight, height):
            return
        
        weight = float(weight)
        height = float(height)
        
        
        bmi = self.calculate_bmi(weight, height)
        category, color = self.categorize_bmi(bmi)
        
        
        result_text = f"BMI: {bmi:.2f}\n\nCategory: {category}\n\n"
        
        if category == "Underweight":
            result_text += "You may need to gain weight. Consult a healthcare provider."
        elif category == "Normal weight":
            result_text += "Great! You're at a healthy weight. Keep it up!"
        elif category == "Overweight":
            result_text += "Consider a balanced diet and regular exercise."
        else:
            result_text += "Please consult a healthcare provider for guidance."
        
        self.result_label.config(text=result_text, fg=color)
        
       
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if username not in self.users_data:
            self.users_data[username] = []
        
        self.users_data[username].append({
            "date": timestamp,
            "weight": weight,
            "height": height,
            "bmi": round(bmi, 2),
            "category": category
        })
        
        if self.save_data():
            messagebox.showinfo("Success", "BMI calculated and saved successfully!")
            self.refresh_history()
            self.refresh_statistics()
    
    def setup_history_tab(self):
        """Setup the history viewing interface"""
        main_frame = tk.Frame(self.history_tab, bg=self.bg_color)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        
        tk.Label(main_frame, text="BMI History", font=("Arial", 20, "bold"), 
                bg=self.bg_color).pack(pady=10)
        
       
        select_frame = tk.Frame(main_frame, bg=self.bg_color)
        select_frame.pack(pady=10)
        
        tk.Label(select_frame, text="Select User:", font=("Arial", 11), 
                bg=self.bg_color).pack(side='left', padx=5)
        
        self.history_user_var = tk.StringVar()
        self.history_user_combo = ttk.Combobox(select_frame, 
                                               textvariable=self.history_user_var,
                                               font=("Arial", 11), width=20, 
                                               state='readonly')
        self.history_user_combo.pack(side='left', padx=5)
        self.history_user_combo.bind('<<ComboboxSelected>>', 
                                     lambda e: self.display_user_history())
        
       
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True, pady=10)
        
       
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
       
        self.history_tree = ttk.Treeview(tree_frame, 
                                         columns=('Date', 'Weight', 'Height', 'BMI', 'Category'),
                                         show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_tree.yview)
        
      
        self.history_tree.heading('Date', text='Date & Time')
        self.history_tree.heading('Weight', text='Weight (kg)')
        self.history_tree.heading('Height', text='Height (cm)')
        self.history_tree.heading('BMI', text='BMI')
        self.history_tree.heading('Category', text='Category')
        
        self.history_tree.column('Date', width=150)
        self.history_tree.column('Weight', width=100)
        self.history_tree.column('Height', width=100)
        self.history_tree.column('BMI', width=80)
        self.history_tree.column('Category', width=120)
        
        self.history_tree.pack(fill='both', expand=True)
        
        
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Delete Selected Entry", 
                 command=self.delete_entry, font=("Arial", 10),
                 bg="#e74c3c", fg="white", padx=10, pady=5).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Clear All History for User", 
                 command=self.clear_user_history, font=("Arial", 10),
                 bg="#e67e22", fg="white", padx=10, pady=5).pack(side='left', padx=5)
        
        self.refresh_history()
    
    def refresh_history(self):
        """Refresh the history dropdown"""
        users = list(self.users_data.keys())
        self.history_user_combo['values'] = users
        if users:
            if not self.history_user_var.get() or self.history_user_var.get() not in users:
                self.history_user_var.set(users[0])
            self.display_user_history()
    
    def display_user_history(self):
        """Display history for selected user"""
        
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        username = self.history_user_var.get()
        if username and username in self.users_data:
            history = self.users_data[username]
            
            if isinstance(history, list):
                for entry in reversed(history):
                    if isinstance(entry, dict):
                        self.history_tree.insert('', 'end', values=(
                            entry.get('date', 'N/A'),
                            entry.get('weight', 'N/A'),
                            entry.get('height', 'N/A'),
                            entry.get('bmi', 'N/A'),
                            entry.get('category', 'N/A')
                        ))
    
    def delete_entry(self):
        """Delete selected history entry"""
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an entry to delete")
            return
        
        if messagebox.askyesno("Confirm", "Delete selected entry?"):
            item = self.history_tree.item(selected[0])
            date = item['values'][0]
            username = self.history_user_var.get()
            
            self.users_data[username] = [e for e in self.users_data[username] 
                                         if e['date'] != date]
            
            if self.save_data():
                self.display_user_history()
                self.refresh_statistics()
                messagebox.showinfo("Success", "Entry deleted successfully")
    
    def clear_user_history(self):
        """Clear all history for selected user"""
        username = self.history_user_var.get()
        if not username:
            return
        
        if messagebox.askyesno("Confirm", 
                              f"Delete all history for {username}?"):
            del self.users_data[username]
            if self.save_data():
                self.refresh_history()
                self.refresh_statistics()
                messagebox.showinfo("Success", "History cleared successfully")
    
    def setup_statistics_tab(self):
        """Setup the statistics and trends interface"""
        main_frame = tk.Frame(self.statistics_tab, bg=self.bg_color)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
       
        tk.Label(main_frame, text="Statistics & Trends", 
                font=("Arial", 20, "bold"), bg=self.bg_color).pack(pady=10)
        
       
        select_frame = tk.Frame(main_frame, bg=self.bg_color)
        select_frame.pack(pady=10)
        
        tk.Label(select_frame, text="Select User:", font=("Arial", 11), 
                bg=self.bg_color).pack(side='left', padx=5)
        
        self.stats_user_var = tk.StringVar()
        self.stats_user_combo = ttk.Combobox(select_frame, 
                                            textvariable=self.stats_user_var,
                                            font=("Arial", 11), width=20, 
                                            state='readonly')
        self.stats_user_combo.pack(side='left', padx=5)
        self.stats_user_combo.bind('<<ComboboxSelected>>', 
                                   lambda e: self.display_statistics())
        
       
        self.stats_info_frame = tk.LabelFrame(main_frame, text="Summary Statistics",
                                             font=("Arial", 11, "bold"), 
                                             bg=self.bg_color, padx=20, pady=20)
        self.stats_info_frame.pack(pady=10, fill='x')
        
        self.stats_label = tk.Label(self.stats_info_frame, text="", 
                                    font=("Arial", 10), bg=self.bg_color, 
                                    justify='left')
        self.stats_label.pack()
        
        
        self.chart_frame = tk.Frame(main_frame, bg='#bbc3ee')
        self.chart_frame.pack(fill='both', expand=True, pady=10)
        
        self.refresh_statistics()
    
    def refresh_statistics(self):
        """Refresh the statistics dropdown"""
        users = list(self.users_data.keys())
        self.stats_user_combo['values'] = users
        if users:
            if not self.stats_user_var.get() or self.stats_user_var.get() not in users:
                self.stats_user_var.set(users[0])
            self.display_statistics()
    
    def display_statistics(self):
        """Display statistics and trends for selected user"""
        username = self.stats_user_var.get()
        
        if not username or username not in self.users_data:
            self.stats_label.config(text="No data available")
          
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            return
        
        data = self.users_data[username]
        
       
        if not isinstance(data, list) or not data:
            self.stats_label.config(text="No data available")
            
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            return
        
       
        bmis = [entry['bmi'] for entry in data if isinstance(entry, dict) and 'bmi' in entry]
        weights = [entry['weight'] for entry in data if isinstance(entry, dict) and 'weight' in entry]
        
        if not bmis or not weights:
            self.stats_label.config(text="No valid data available")
            
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            return
        
        avg_bmi = sum(bmis) / len(bmis)
        min_bmi = min(bmis)
        max_bmi = max(bmis)
        latest_bmi = bmis[-1]
        
        avg_weight = sum(weights) / len(weights)
        weight_change = weights[-1] - weights[0] if len(weights) > 1 else 0
        
       
        stats_text = f"""
Total Entries: {len(data)}
Latest BMI: {latest_bmi:.2f}
Average BMI: {avg_bmi:.2f}
Lowest BMI: {min_bmi:.2f}
Highest BMI: {max_bmi:.2f}

Average Weight: {avg_weight:.2f} kg
Weight Change: {weight_change:+.2f} kg
        """
        
        self.stats_label.config(text=stats_text)
        
        
        self.create_trend_chart(data)
    
    def create_trend_chart(self, data):
        """Create BMI trend chart"""
        
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        if len(data) < 2:
            tk.Label(self.chart_frame, text="Need at least 2 entries to show trends",
                    font=("Arial", 12), bg='#bbc3ee').pack(expand=True)
            return
        
        
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        
        dates = [entry['date'].split()[0] for entry in data]
        bmis = [entry['bmi'] for entry in data]
        
        
        ax.plot(dates, bmis, marker='o', linewidth=2, markersize=8, 
               color=self.secondary_color)
        ax.axhline(y=18.5, color='#3498db', linestyle='--', alpha=0.5, label='Underweight')
        ax.axhline(y=25, color='#2ecc71', linestyle='--', alpha=0.5, label='Normal')
        ax.axhline(y=30, color='#f39c12', linestyle='--', alpha=0.5, label='Overweight')
        
        ax.set_xlabel('Date', fontsize=10)
        ax.set_ylabel('BMI', fontsize=10)
        ax.set_title('BMI Trend Over Time', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=8)
        
      
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        fig.tight_layout()
        
       
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()