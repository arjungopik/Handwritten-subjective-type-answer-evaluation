from sentence_transformers import SentenceTransformer,util
model = SentenceTransformer('all-MiniLM-L6-v2')    
semantic_model = SentenceTransformer('clips/mfaq')



marks = [0]*10
answer = "Computer science encompasses a diverse array of concepts crucial for understanding and advancing technology. The study of algorithms, data structures, and computational theory enables efficient problem-solving across various domains. Understanding the principles underlying computer networks is essential for designing reliable and secure communication systems. Development of artificial intelligence and machine learning algorithms empowers systems to perform tasks requiring human-like intelligence, driving innovations in fields such as robotics and natural language processing. Cybersecurity plays a critical role in protecting computer systems, networks, and data from unauthorized access and cyber threats, ensuring the integrity and privacy of digital information. Amidst these advancements, it's intriguing to note unrelated phenomena, such as the migration patterns of monarch butterflies being influenced by lunar cycles or ancient beliefs about lightning being the result of divine clashes. Similarly, the flavor of fruit isn't determined by its skin color, and octopuses' reputation as escape artists in aquariums seems far removed from the world of computer science. Yet, such unrelated tidbits add richness to our understanding of the world, juxtaposed against the rigor and precision of computer science principles."
answers = list(answer.split('.'))
print(answers)
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



answerEmbeddings = model.encode(answers)
KeyEmbeddings = model.encode(keys)


DictAnswerEmbeddings = {}
DictKeyEmbeddings  = {}

for i in range(len(keys)):
    for j in range(i+1,len(answers)-1):
        cos = util.cos_sim(KeyEmbeddings[i],answerEmbeddings[j])
        if cos > 0.55:
            if i in DictKeyEmbeddings:
                query_embedding = DictKeyEmbeddings[i]
            else:
                query_embedding = semantic_model.encode(keys[i])
                DictKeyEmbeddings[i] = query_embedding
            if j in DictAnswerEmbeddings:
                answer_embedding = DictAnswerEmbeddings[j]
            else:
                answer_embedding = semantic_model.encode(answers[j])
                DictAnswerEmbeddings[j] = answer_embedding            
            semscore= util.semantic_search(query_embedding,answer_embedding)
            semvalue = semscore[0][0]['score']
            if semvalue > 0.90:
                marks[i]=1
                break
    
            



final_grade =0
for val in marks:
    final_grade += val

print("final score  = ",final_grade)
