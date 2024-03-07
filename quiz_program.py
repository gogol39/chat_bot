import json
import urllib.request

def get_questions(amount=10):
    url = f"https://opentdb.com/api.php?amount={amount}&difficulty=easy"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    return data['results']

def play_quiz(questions):
    score = 0
    for idx, question in enumerate(questions, 1):
        question_text = f"Question {idx}: {question['question']}"
        answers = question['incorrect_answers'] + [question['correct_answer']]
        answers.sort()
        options = "\n".join([f"{i}. {answer}" for i, answer in enumerate(answers, 1)])
        question_text += "\n\nOptions:\n" + options
        print(question_text)

        user_answer = None
        while user_answer is None:
            user_input = input("Your answer: ").strip()
            if user_input.lower() == "exit":
                print("Game over.")
                return

            try:
                user_answer = int(user_input)
                if user_answer < 1 or user_answer > len(answers):
                    raise ValueError
            except ValueError:
                print("Invalid input. Please enter a valid option number.")
                continue

        correct_answer = question['correct_answer']
        if user_answer == answers.index(correct_answer) + 1:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! Correct answer: {correct_answer}")

    print(f"Game over! Your final score: {score}/{len(questions)}")

def main():
    num_questions = 5
    questions = get_questions(num_questions)
    play_quiz(questions)

if __name__ == "__main__":
    main()
