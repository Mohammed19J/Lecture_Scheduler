# Lecture Scheduler

## **Description**
The **Lecture Scheduler** is a comprehensive web application designed to help users manage and organize their lecture schedules efficiently. The app ensures no overlapping lectures and optimizes the schedule for ease of access and clarity. It provides features like adding, deleting, and visualizing weekly lectures.

This app was initially developed as a Python desktop application using **Tkinter**. Later, it was ported to **React**, reusing the recursive scheduling algorithm for optimization.

The React version of the app takes advantage of modern web technologies, offering a sleek, responsive UI and the ability to deploy on the web using **GitHub Pages**.

---

## **Features**
- Add and delete lectures with details like day, time, lecturer, and room number.
- Ensure no overlapping lectures using an optimized recursive algorithm.
- Visualize the weekly schedule in an accessible and color-coded layout.
- Responsive design with dark mode support.

---

## **Tech Stack**

### **Frontend**
- **React**: For building the user interface.
- **Tailwind CSS**: For styling the components.
- **React Hot Toast**: For notifications.
- **Heroicons**: For icons.

### **Backend Algorithm**
- **Recursive Scheduling**: A recursive algorithm to ensure no lectures overlap. The algorithm traverses through all possible combinations to find the optimal schedule.

### **Initial Version**
- **Python**: Used for prototyping with Tkinter for the desktop UI.
- **Algorithm**: The same recursive logic was implemented in Python, providing the backbone for the React app.

---

## **How the Recursive Algorithm Works**
The recursive scheduling algorithm ensures there are no overlapping lectures by:
1. Sorting lectures by their start time.
2. Iteratively and recursively trying to fit each lecture into the schedule.
3. Skipping lectures that overlap with already-scheduled ones.
4. Backtracking when a conflict is detected and exploring alternative configurations.

The algorithm guarantees that the solution is optimal, or it notifies the user if no valid schedule exists.

---

## **Try It Out**
If you would like to try the app for yourself, please click the link below:

🔗 [Lecture Scheduler - Live Demo](https://mohammed19j.github.io/Lecture_Scheduler/)

---
