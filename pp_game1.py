import tkinter as tk  
import random  

class PingPongGame:  
    def __init__(self, master):  
        self.master = master  
        self.master.title("Ping Pong Game")  
        self.master.geometry("600x400")  

        self.canvas = tk.Canvas(self.master, bg="black", width=600, height=400)  
        self.canvas.pack()  

        self.score = 0  # Initialize the score to 0  
        self.hit_count = 0  # Counter for how many times the paddle has been hit  
        # Position the score text at the top center in green  
        self.score_text = self.canvas.create_text(300, 20, text=f"Score: {self.score}", fill="green", font=("Helvetica", 20))  

        self.difficulty_increase_score = 5  # Score at which difficulty increases  
        self.difficulty_multiplier = 1.0  # Starting difficulty multiplier  

        self.initialize_game()  

    def initialize_game(self):  
        self.canvas.delete("all")  # Clear previous game components  

        # Reset score and difficulty on new game  
        self.score = 0  
        self.hit_count = 0  # Reset hit count  
        self.difficulty_multiplier = 1.0  # Reset difficulty multiplier  
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")  # Display the initial score of 0  

        # Initial positions and settings  
        self.paddle = self.canvas.create_rectangle(250, 350, 350, 370, fill="white")  
        self.ball = self.canvas.create_oval(290, 200, 310, 220, fill=self.get_random_color())  # Set initial random color  
        self.ball_dx = random.choice([-3, 3]) * self.difficulty_multiplier  
        self.ball_dy = -3 * self.difficulty_multiplier  

        self.canvas.bind("<Key>", self.on_key_press)  
        self.canvas.focus_set()  

        self.move_ball()  

        # Clear the game over message if it exists  
        self.canvas.delete("game_over")  

    def on_key_press(self, event):  
        key = event.keysym  
        if key == "Left":  
            self.move_paddle(-20)  
        elif key == "Right":  
            self.move_paddle(20)  

    def move_paddle(self, delta):  
        coords = self.canvas.coords(self.paddle)  
        if coords[0] + delta >= 0 and coords[2] + delta <= 600:  
            self.canvas.move(self.paddle, delta, 0)  

    def move_ball(self):  
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)  
        ball_coords = self.canvas.coords(self.ball)  
        paddle_coords = self.canvas.coords(self.paddle)  

        # Ball hits the top  
        if ball_coords[1] <= 0:  
            self.ball_dy = -self.ball_dy  

        # Ball hits the left or right wall  
        if ball_coords[0] <= 0 or ball_coords[2] >= 600:  
            self.ball_dx = -self.ball_dx  

        # Ball hits the paddle  
        if (paddle_coords[0] < ball_coords[2] < paddle_coords[2]) and (paddle_coords[1] < ball_coords[3] < paddle_coords[3]):  
            self.ball_dy = -self.ball_dy  
            self.score += 1  # Increment the score  
            self.hit_count += 1  # Increment the hit count  
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")  # Update the score display  

            # Change the color of the score text every 5 hits  
            if self.hit_count % 5 == 0:  
                self.canvas.itemconfig(self.score_text, fill=self.get_random_color())  

            # Increase difficulty based on score  
            if self.score % self.difficulty_increase_score == 0:  
                self.difficulty_multiplier += 0.2  # Increase difficulty  
                self.ball_dx = 3 * self.difficulty_multiplier if self.ball_dx > 0 else -3 * self.difficulty_multiplier  
                self.ball_dy = -3 * self.difficulty_multiplier  

        # Ball falls below the paddle (Game Over)  
        if ball_coords[3] >= 400:  
            self.game_over()  
            return  

        # Continue moving the ball  
        self.master.after(20, self.move_ball)  

    def get_random_color(self):  
        """ Generate a random color in hex format. """  
        return f'#{random.randint(0, 0xFFFFFF):06x}'  

    def game_over(self):  
        self.canvas.create_text(300, 200, text="Game Over", fill="white", font=("Helvetica", 30), tags="game_over")  
        self.canvas.create_text(300, 250, text=f"Final Score: {self.score}", fill="green", font=("Helvetica", 20), tags="game_over")  
        self.canvas.create_text(300, 280, text="Press R to Try Again", fill="white", font=("Helvetica", 15), tags="game_over")  
        self.canvas.bind("<Key>", self.restart_game)  

    def restart_game(self, event):  
        if event.keysym == 'r':  
            self.initialize_game()  # Start a new game  

if __name__ == "__main__":  
    root = tk.Tk()  
    game = PingPongGame(root)  
    root.mainloop()
 #done