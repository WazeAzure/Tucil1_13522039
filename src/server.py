from flask import Flask, render_template, request, url_for, flash
import os
import numpy as np
import json

import main
import Solution

m_obj = None
sol = None

app = Flask(__name__)

abs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/save-file', methods=['POST'])
def saveFile():
    result_file = sol.saveToFile(request.form.get('filename'))
    return json.dumps({'success':True, 'fname': result_file}), 200, {'ContentType':'application/json'} 

@app.route('/solve', methods=['POST'])
def solve():
    global sol, m_obj

    m_obj = main.App()
    if "auto-generate" in request.form:
        print("go to auto generate")
        m_obj.rf.choice = 2
        arr = ['buffer-size', 'token-size', 'token-id', 'matrix-col', 'matrix-row', 'seq-id', 'seq-len', 'seq-min', 'seq-max']
        
        for x in arr:
            if x not in request.form:
                flash(f'{x} is required!')

        buffer_size = int(request.form['buffer-size'])
        token_size = int(request.form['token-size'])
        token = np.array(request.form['token-id'].split(' '))
        token = token[token != '']
        matrix_size = (int(request.form['matrix-row']), int(request.form['matrix-col']))
        seq_size = int(request.form['seq-id'])
        seq_len = int(request.form['seq-len'])
        min_score = int(request.form['seq-min'])
        max_score = int(request.form['seq-max'])

        print("buffer size:", buffer_size)
        m_obj.rf.generate_problem(buffer_size, matrix_size, token_size, token, seq_size, seq_len, min_score, max_score)
        print("buffer size:", m_obj.rf.buffer_size)
        sol = Solution.Solution(m_obj.rf.matrix_size, m_obj.rf.sequence, m_obj.rf.matrix, m_obj.rf.buffer_size)
        print("maximum depth:", sol.max_depth)
        sol.main()
    elif "submit" in request.form:
        arr = ['buffer-size', 'matrix', 'seq-score']
        for x in arr:
            if x not in request.form:
                flash(f'{x} is required!')

        m_obj.rf.buffer_size = int(request.form['buffer-size'])
        matrix = request.form['matrix'].split('\n')
        m_obj.rf.matrix = list(map(lambda x: [y for y in x.strip('\r').split(' ') if  y], matrix))
        # matrix = matrix[matrix != '']
        m_obj.rf.sequence = []
        seq_score = request.form['seq-score'].split('\n')
        for i in range(len(seq_score) // 2):
            seq, val = seq_score[2*i].strip('\r'), int(seq_score[1 + i*2].strip('\r'))
            m_obj.rf.sequence.append(([y for y in seq.split(' ') if y], val))
        m_obj.rf.sequence_size = len(m_obj.rf.sequence)
        
        m_obj.rf.matrix_size = [len(m_obj.rf.matrix), len(m_obj.rf.matrix[0])]
        sol = Solution.Solution(m_obj.rf.matrix_size, m_obj.rf.sequence, m_obj.rf.matrix, m_obj.rf.buffer_size)
        sol.main()
    elif "file-solve" in request.form:
        if "file-name" not in request.form:
            flash("filename is required!")
        
        filename = request.form['file-name']
        m_obj.rf.read_file(filename)

        sol = Solution.Solution(m_obj.rf.matrix_size, m_obj.rf.sequence, m_obj.rf.matrix, m_obj.rf.buffer_size)
        sol.main()

    
    between = []

    for i in range(len(sol.max_coor)-1):
        a, b = sol.max_coor[i], sol.max_coor[i+1]
        
        if(a[0] == b[0]):
            start_col = min(a[1], b[1])
            end_col = max(a[1], b[1])

            for j in range(start_col, end_col+1):
                between.append((a[0], j))
        elif(a[1] == b[1]):
            start_r = min(a[0], b[0])
            end_r = max(a[0], b[0])

            for j in range(start_r, end_r):
                between.append((j, a[1]))
    
    return render_template('solution.html', matrix=m_obj.rf.matrix, sequence=m_obj.rf.sequence,
                           matrix_size=m_obj.rf.matrix_size, max_score=sol.max_score, coordinates=sol.max_coor,
                           exec_time=round(sol.time_elapsed * 1000, 2), len_coor=len(sol.max_coor), between=between)

if __name__ == "__main__":
    app.run(debug=True)