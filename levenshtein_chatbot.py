import pandas as pd


class LevenshteinChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    def get_initial_matrix(self, x_len, y_len):  # x, y의 길이를 받아
        # x의 길이로 빈 2차 배열 생성 # ex) x=3,  [ [], [], [] ]
        matrix = [[] for i in range(x_len+1)]
        for i in range(x_len+1):
            # y 길이로 각 원소 초기화 # ex) y=4, [ [0,0,0,0], [0,0,0,0], [0,0,0,0] ]
            matrix[i] = [0 for j in range(y_len+1)]
        for i in range(x_len+1):  # [ [0,0,0,0], [1,0,0,0], [2,0,0,0]  ]
            matrix[i][0] = i
        for j in range(y_len+1):  # [ [0,1,2,3], [1,0,0,0], [2,0,0,0]  ]
            matrix[0][j] = j
        return matrix

    def calc_distance(self, a, b):
        ''' 레벤슈타인 거리 계산하기 '''
        if a == b:
            return 0  # 같으면 0을 반환
        a_len = len(a)  # a 길이
        b_len = len(b)  # b 길이
        if a == "":
            return b_len
        if b == "":
            return a_len

        # 초기화된 행렬 구하기
        matrix = self.get_initial_matrix(a_len, b_len)

        for i in range(1, a_len+1):
            ac = a[i-1]  # ac : 앞글자
            for j in range(1, b_len+1):
                bc = b[j-1]  # bc : 앞글자
                # a문장의 앞글자, b문장의 앞글자가 같다면 비용은 0에서 시작한다 다르면 1부터 시작한다
                cost = 0 if (ac == bc) else 1
                matrix[i][j] = min([
                    matrix[i-1][j] + 1,  # 문자 제거: 위쪽에서 +1
                    matrix[i][j-1] + 1,  # 문자 삽입: 왼쪽 수에서 +1
                    # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
                    matrix[i-1][j-1] + cost
                ])
        return matrix[a_len][b_len]

    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers

    def find_best_answer(self, input_sentence):
        similarities = [self.calc_distance(input_sentence, q)
                        for q in self.questions]  # input_sentence 와 레벤슈타인 거리를 계산해 배열에 저장
        best_match_index = similarities.index(
            min(similarities))  # 레벤슈타인 거리 최소값의 인덱스를 구함
        return self.answers[best_match_index]  # 해당 인덱스의 답변을 반환


# CSV 파일 경로를 지정하세요.
filepath = 'ChatbotData.csv'

# 간단한 챗봇 인스턴스를 생성합니다.
Lchatbot = LevenshteinChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('당신 : ')
    if input_sentence.lower() == '종료':
        break
    response = Lchatbot.find_best_answer(input_sentence)
    print('챗봇:', response)
