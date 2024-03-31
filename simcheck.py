from sentence_transformers import SentenceTransformer, util

# Load models
model = SentenceTransformer('all-MiniLM-L6-v2')
semantic_model = SentenceTransformer('clips/mfaq')

# Read answers from file
with open("output.txt", "r") as file:
    answer = file.read()

# Split the answers into a list
answers = answer.split('.')

# Define keys
keys = ['Study of algorithms for problem-solving.',
        'Organization and manipulation of data efficiently.',
        'Various approaches to problem-solving in programming.',
        'Analysis of resources required by algorithms.',
        'Design and organization of computer systems.',
        'Management of hardware resources by operating systems.',
        'Principles and protocols underlying computer networks.',
        'Development of systems performing tasks requiring human intelligence.',
        'Protection of computer systems, networks, and data.',
        'Principles and practices for developing reliable software solutions.']

# Encode answers and keys
answerEmbeddings = model.encode(answers)
KeyEmbeddings = model.encode(keys)

# Initialize marks list
marks = [0] * len(keys)

# Compare embeddings and update marks
for i in range(len(keys)):
    for j in range(len(answers)):
        cos = util.cos_sim(KeyEmbeddings[i], answerEmbeddings[j])
        if cos > 0.55:
            query_embedding = semantic_model.encode(keys[i])
            answer_embedding = semantic_model.encode(answers[j])
            semscore = util.semantic_search(query_embedding, answer_embedding)
            semvalue = semscore[0][0]['score']
            if semvalue > 0.90:
                marks[j] = 1

# Calculate final grade
final_grade = sum(marks)

print("Marks:", marks)
print("Final score:", final_grade)
