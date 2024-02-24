import copy

### nonogram solver
### uses row and col hints to automatically solve a nonogram puzzle
class nonogram_solver:
    def __init__(self, rows_hints, cols_hints):
        self.size = (len(rows_hints), len(cols_hints))
        self.rows_hints = rows_hints 
        self.cols_hints = cols_hints
        self.board = [[None for x in range(len(cols_hints))] for y in range(len(rows_hints))]
        self.moves = 0

    ### obtain continuous sequences of true (known painted), false (known unpainted), and none (unknown) 
    def update_sequences(self):
        self.seq_lengths = [] # length of each sequence
        self.seq_types = [] # type of each sequence 
        seq_iter = 0
        prev_type = None
        for i in range(self.line_length):

            # compare types of subsequent squares
            if self.is_row:
                cur_type = self.board[self.line_idx][i]
                is_match = cur_type == prev_type or (cur_type is None and prev_type is None)
                prev_type = cur_type
            else:
                cur_type = self.board[i][self.line_idx]
                is_match = cur_type == prev_type or (cur_type is None and prev_type is None)
                prev_type = cur_type

            # update seq_types and seq_lengths
            if i == 0:
                self.seq_types.append(prev_type)
                self.seq_lengths.append(1)
            elif is_match:
                self.seq_lengths[seq_iter] += 1
            else:
                self.seq_types.append(prev_type)
                self.seq_lengths.append(1)
                seq_iter += 1

    ### determine remaining section of line (row or col) and hints that still need to be checked
    ### i.e. ignore known unpainted squares and completed hints on ends/edges of lines
    def update_edges(self):

        # left or top edge
        self.min_hints_idx = 0
        self.min_line_idx = 0
        for i in range(len(self.seq_types)):
            if self.seq_types[i] == None:
                break
            elif self.seq_types[i]:
                if self.seq_lengths[i] == self.line_hints[self.min_hints_idx]: # painted sequence is complete
                    self.min_hints_idx += 1
                else:
                    break
            self.min_line_idx += self.seq_lengths[i]

        # right or bottom edge
        self.max_hints_idx = len(self.line_hints) - 1
        self.max_line_idx = self.line_length - 1
        for i in range(len(self.seq_types)-1, -1, -1):
            if self.seq_types[i] == None:
                break
            elif self.seq_types[i]:
                if self.seq_lengths[i] == self.line_hints[self.max_hints_idx]: # painted sequence is complete
                    self.max_hints_idx -= 1
                else:
                    break
            self.max_line_idx -= self.seq_lengths[i]

    ### paints central sections of hints based on the length of the unfinished section of line
    ### and the minimum number of painted and interrupting squares in that unfinished line
    def squeeze_paint(self):

        # determine number of squares unaccounted for by required painted and interrupting squares
        num_accounted_squares = 0
        for i in range(self.min_hints_idx, self.max_hints_idx + 1): 
            num_accounted_squares += self.line_hints[i] 
        num_accounted_squares += self.max_hints_idx - self.min_hints_idx 
        unfinished_line_length = self.max_line_idx - self.min_line_idx + 1
        num_unaccounted_squares = unfinished_line_length - num_accounted_squares 

        # paint squares known to belong to a particular sequence
        start_idx = num_unaccounted_squares + self.min_line_idx # where to start painting section of current hint, if possible
        for i in range(self.min_hints_idx, self.max_hints_idx + 1):
            if self.line_hints[i] > num_unaccounted_squares: 
                for j in range(start_idx, start_idx + (self.line_hints[i] - num_unaccounted_squares)):
                    if self.is_row:
                        self.board[self.line_idx][j] = True
                    else:
                        self.board[j][self.line_idx] = True
            start_idx += 1 + self.line_hints[i]

    ### eliminate edges that aren't long enough to contain first or last hints 
    ### based on known unpainted squares near edges
    def eliminate_edges(self):

        # left or top edge
        start_idx = 0
        for i in range(len(self.seq_lengths)-1):
            if self.seq_types[i] or self.seq_types[i + 1]: # painted square reached before unpainted
                break
            elif self.seq_types[i] == None and self.seq_types[i + 1] == False:
                if self.seq_lengths[i] < self.line_hints[0]: # not enough space for first hint
                    for j in range(start_idx, start_idx + self.seq_lengths[i]):
                        if self.is_row:
                            self.board[self.line_idx][j] = False
                        else:
                            self.board[j][self.line_idx] = False
                else:
                    break
            start_idx += self.seq_lengths[i]

        # right or bottom edge
        start_idx = self.line_length - 1
        for i in range(len(self.seq_lengths) - 1, 0, -1):
            if self.seq_types[i] or self.seq_types[i - 1]: # painted square reached before unpainted
                break
            elif self.seq_types[i] == None and self.seq_types[i - 1] == False:
                if self.seq_lengths[i] < self.line_hints[len(self.line_hints) - 1]: # not enough space for last hint
                    for j in range(start_idx, start_idx - self.seq_lengths[i], -1):
                        if self.is_row:
                            self.board[self.line_idx][j] = False
                        else:
                            self.board[j][self.line_idx] = False
            start_idx -= self.seq_lengths[i]

    ### "pull" or eliminate edges that can't contain first or last hints and
    ### "push" or paint squares that must be part of first or last hints 
    ### based on length of painted sequences and their proximity to the edges
    def pull_edges_push_paint(self):

        # left or top edge
        max_min_trigger_idx = self.min_line_idx + self.line_hints[self.min_hints_idx] # max index for pull/push effects at left/top (min) edge
        first_paint_idx = 0
        num_first_paint = -1
        line_hints_idx = 0

         # find closest paint sequence to edge
        for i in range(len(self.seq_types)):
            if self.seq_types[i] == False or self.seq_types[i] == None \
                    or line_hints_idx < self.min_hints_idx:
                first_paint_idx += self.seq_lengths[i]
                if self.seq_types[i]:
                    line_hints_idx += 1
            else:
                num_first_paint = self.seq_lengths[i]
                break

        if num_first_paint != -1:
            if first_paint_idx == max_min_trigger_idx:
                # pull edge
                for i in range(self.min_line_idx, self.min_line_idx + num_first_paint):
                    if self.is_row:
                        self.board[self.line_idx][i] = False
                    else:
                        self.board[i][self.line_idx] = False
            if first_paint_idx < max_min_trigger_idx - 1: 
                # push paint
                for i in range(first_paint_idx, max_min_trigger_idx):
                    if self.is_row:
                        self.board[self.line_idx][i] = True
                    else:
                        self.board[i][self.line_idx] = True

        # right or bottom edge
        min_max_trigger_idx = self.max_line_idx - self.line_hints[self.max_hints_idx] # min index for pull/push effects at right/bottom (max) edge
        first_paint_idx = self.line_length - 1
        num_first_paint = -1
        line_hints_idx = len(self.line_hints)-1

        # find closest paint sequence to edge
        for i in range(len(self.seq_types) - 1, -1, -1): 
            if self.seq_types[i] == False or self.seq_types[i] == None \
                    or line_hints_idx > self.max_hints_idx:
                first_paint_idx -= self.seq_lengths[i]
                if self.seq_types[i]:
                    line_hints_idx -= 1
            else:
                num_first_paint = self.seq_lengths[i]
                break

        if num_first_paint != -1:
            if first_paint_idx == min_max_trigger_idx: 
                # pull edge
                for i in range(self.max_line_idx, self.max_line_idx - num_first_paint, -1):
                    if self.is_row:
                        self.board[self.line_idx][i] = False
                    else:
                        self.board[i][self.line_idx] = False
            if first_paint_idx > min_max_trigger_idx + 1: 
                # pull edge
                for i in range(first_paint_idx, min_max_trigger_idx, -1):
                    if self.is_row:
                        self.board[self.line_idx][i] = True
                    else:
                        self.board[i][self.line_idx] = True

    ### interrupt completed hints with unpainted squares
    def interrupt_completed_hints(self):

        # left or top edge
        other_line_idx = 0
        line_hints_idx = 0
        for i in range(len(self.seq_types)):
            other_line_idx += self.seq_lengths[i]
            if self.seq_types[i] == None: # later paint sequences may not correspond to hints
                break
            elif self.seq_types[i]:
                if self.line_hints[line_hints_idx] == self.seq_lengths[i]:
                    # eliminate square following completed paint sequence
                    line_hints_idx += 1
                    if other_line_idx < self.line_length:
                        if self.is_row:
                            self.board[self.line_idx][other_line_idx] = False
                        else:
                            self.board[other_line_idx][self.line_idx] = False
                else: # current paint sequence is incomplete
                    break

        # right or bottom edge
        other_line_idx = self.line_length-1
        line_hints_idx = len(self.line_hints)-1
        for i in range(len(self.seq_types)-1, -1, -1):
            other_line_idx -= self.seq_lengths[i]
            if self.seq_types[i] == None: # later paint sequences may not correspond to hints
                break
            elif self.seq_types[i]:
                if self.line_hints[line_hints_idx] == self.seq_lengths[i]:
                    # eliminate square following completed paint sequence
                    line_hints_idx -= 1
                    if other_line_idx >= 0:
                        if self.is_row:
                            self.board[self.line_idx][other_line_idx] = False
                        else:
                            self.board[other_line_idx][self.line_idx] = False
                else: # current paint sequence is incomplete
                    break
    
    ### helper function for eliminate_generic and paint_generic. 
    ### attempts to find a valid solution for the given test_line, which
    ### contains one assumed value. 
    ### returns True once a valid solution is found, or False if all attempts fail
    def test_validity(self, test_line, start_idx=0, line_hints_idx=0):

        # test hint in all squares in line starting at start_idx
        for i in range(start_idx, self.line_length):
            copy_test_line = copy.deepcopy(test_line)
            hint = self.line_hints[line_hints_idx]
            is_valid = True
            # test if hint fits here
            for j in range(i, i + hint):
                if j >= self.line_length:
                    is_valid = False
                    break
                if copy_test_line[j] == None:
                    copy_test_line[j] = True
                elif copy_test_line[j] == False:
                    is_valid = False
                    break

            if not is_valid: # try again with successive placement of hint
                continue
            elif line_hints_idx < len(self.line_hints) - 1:
                # recursively attempt to fit all hints in test_line
                is_valid = self.test_validity(copy_test_line, i + hint + 1, line_hints_idx + 1)
                if is_valid:
                    return True
            else:
                # check for false positive: painted sequences should match hints 
                painted_seq_len = 0
                cur_hints_idx = 0
                for j in range(self.line_length):
                    if copy_test_line[j]:
                        painted_seq_len += 1
                    elif (copy_test_line[j] == False or copy_test_line[j] == None) \
                            and painted_seq_len > 0:
                        if cur_hints_idx >= len(self.line_hints):
                            is_valid = False
                            break
                        if painted_seq_len != self.line_hints[cur_hints_idx]:
                            is_valid = False
                            break
                        else:
                            cur_hints_idx += 1
                        painted_seq_len = 0

                # edge case
                if cur_hints_idx >= len(self.line_hints) and painted_seq_len > 0:
                    is_valid = False
                if (cur_hints_idx < len(self.line_hints) and painted_seq_len != self.line_hints[cur_hints_idx]) \
                        or cur_hints_idx < len(self.line_hints) - 1:
                    is_valid = False
                if is_valid:
                    return True
        return False # no valid solution found after all possible attempts

    ### generic elimination function. assumes unknown squares are painted and calls 
    ### test_validity, searching for a contradiction. if one is found, eliminate square.
    ### combined with paint_generic is sufficient to complete puzzle (inefficiently)
    def eliminate_generic(self):
        invalid_indices = []

        # test "True" hypothesis for unknown squares in line
        for i in range(self.line_length):
            if self.is_row:
                test_line = copy.deepcopy(self.board[self.line_idx])
            else:
                test_line = copy.deepcopy([self.board[g][self.line_idx] for g in range(len(self.board))])
            if test_line[i] == None: 
                test_line[i] = True
                is_valid = self.test_validity(test_line)
                if not is_valid:
                    invalid_indices.append(i)

        # eliminate squares that resulted in a contradiction with "True" test
        for i in invalid_indices:
            if self.is_row:
                self.board[self.line_idx][i] = False
            else:
                self.board[i][self.line_idx] = False

    ### generic painting function. assumes unknown squares are unpainted and calls 
    ### test_validity, searching for a contradiction. if one is found, paint square.
    ### combined with eliminate_generic is sufficient to complete puzzle (inefficiently)
    def paint_generic(self):
        invalid_indices = []

        # test "False" hypothesis for unknown squares in line
        for i in range(self.line_length):
            if self.is_row:
                test_line = copy.deepcopy(self.board[self.line_idx])
            else:
                test_line = copy.deepcopy([self.board[g][self.line_idx] for g in range(len(self.board))])
            if test_line[i] == None:
                test_line[i] = False
                is_valid = self.test_validity(test_line)
                if not is_valid:
                    invalid_indices.append(i)

        # paint squares that resulted in a contradiction with "False" test
        for i in invalid_indices:
            if self.is_row:
                self.board[self.line_idx][i] = True
            else:
                self.board[i][self.line_idx] = True

    ### if all hints are satisfied, and thus the line is completed,
    ### eliminate remaining unknown squares
    def clear_completed(self):
        is_complete = True
        line_hints_idx = 0
        num_painted_seqs = 0

        # is_complete if hints satisfied and correct number of sequences
        for i in range(len(self.seq_lengths)):
            if self.seq_types[i]:
                num_painted_seqs += 1
                if num_painted_seqs > len(self.line_hints):
                    break
                if self.seq_lengths[i] != self.line_hints[line_hints_idx]:
                    is_complete = False
                    break
                else:
                    line_hints_idx += 1
        if num_painted_seqs != len(self.line_hints):
            is_complete = False

        if is_complete:
            # eliminate remaining unknown squares in line
            for i in range(self.line_length):
                if self.is_row:
                    if self.board[self.line_idx][i] == None:
                        self.board[self.line_idx][i] = False
                else:
                    if self.board[i][self.line_idx] == None:
                        self.board[i][self.line_idx] = False

    ### print current state of board 
    def print_board(self):
        max_num_col_hints = 0
        max_num_row_hints = 0
        for i in range(self.size[1]):
            if len(self.cols_hints[i]) > max_num_col_hints:
                max_num_col_hints = len(self.cols_hints[i])
        for i in range(self.size[0]):
            if len(self.rows_hints[i]) > max_num_row_hints:
                max_num_row_hints = len(self.rows_hints[i])

        for i in range(max_num_col_hints):
            for j in range(max_num_row_hints + 2):
                print("  ", end="")
            for j in range(self.size[1]):
                if len(self.cols_hints[j]) > i:
                    if self.cols_hints[j][i] < 10:
                        print(self.cols_hints[j][i], end=" ")
                    else:
                        print(self.cols_hints[j][i], end="")
                else:
                    print("  ", end="")
            print()
        for j in range(max_num_row_hints):
            print("  ", end="")
        print("    ", end="")
        for i in range(self.size[1]):
            print("__",end="")
        print("\n")

        for j in range(self.size[0]):
            for i in range(max_num_row_hints):
                if len(self.rows_hints[j]) > i:
                    if self.rows_hints[j][i] < 10:
                        print(self.rows_hints[j][i], end=" ")
                    else:
                        print(self.rows_hints[j][i], end="")
                else:
                    print("  ", end="")
            print(" |  ", end="")
            for i in range(self.size[1]):
                if self.board[j][i] == None:
                    print("  ", end="")
                elif self.board[j][i]:
                    print("# ", end="")
                else:
                    print(". ", end="")
            print()
        print("\n")

    ### run all functions on current line to eliminate and paint squares
    def update_line(self):
        # update current line_length and line_hints
        if self.is_row:
            self.line_hints = self.rows_hints[self.line_idx]
            self.line_length = self.size[1] 
        else:
            self.line_hints = self.cols_hints[self.line_idx]
            self.line_length = self.size[0] 

        # run all functions on current line
        self.update_sequences()
        self.update_edges()
        self.squeeze_paint()

        self.update_sequences()
        self.eliminate_edges()

        self.update_sequences()
        self.update_edges()
        if self.min_hints_idx < len(self.line_hints) and self.max_hints_idx > 0:
            self.pull_edges_push_paint()

        self.update_sequences()
        self.clear_completed()

        self.update_sequences()
        self.interrupt_completed_hints()
        
        self.eliminate_generic()
        self.paint_generic()
        #self.print_board()

    ### run nonogram solver by repeatedly calling update_line on all rows and cols until board is complete
    def run_solver(self):
        incomplete = True
        while incomplete:
            # cols
            self.is_row = False
            for i in range(self.size[1]):
                self.line_idx = i
                self.update_line()
            # rows
            self.is_row = True
            for i in range(self.size[0]): 
                self.line_idx = i
                self.update_line()
            # check if board is complete
            incomplete = False
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] == None:
                        incomplete = True
        self.print_board() # print completed board

### take row and col hints from user and convert to lists
def user_input():
    rows = input("Enter row values, rows separated by commas:\n")
    cols = input("Enter col values, cols separated by commas:\n")
    print()

    # parse row values/hints
    rows_hints = [[]]
    cur_num = ""
    hints_iter = 0
    i = 0
    for char in rows:
        if char == " ":
            rows_hints[hints_iter].append(int(cur_num))
            cur_num = ""
        elif char == ",":
            rows_hints[hints_iter].append(int(cur_num))
            rows_hints.append([])
            cur_num = ""
            hints_iter += 1
        else:
            cur_num += char
            if i == len(rows) - 1:
                rows_hints[hints_iter].append(int(cur_num))
        i += 1

    # parse col values/hints
    cols_hints = [[]]
    cur_num = ""
    hints_iter = 0
    i = 0
    for char in cols:
        if char == " ":
            cols_hints[hints_iter].append(int(cur_num))
            cur_num = ""
        elif char == ",":
            cols_hints[hints_iter].append(int(cur_num))
            cols_hints.append([])
            cur_num = ""
            hints_iter += 1
        else:
            cur_num += char
            if i == len(cols) - 1:
                cols_hints[hints_iter].append(int(cur_num))
        i += 1
    return rows_hints, cols_hints

### repeatedly run nonogram solver, requesting user input for row and col hints 
### (values/numbers from nonogram board)
while True:
    rows_hints, cols_hints = user_input()
    ng_solver = nonogram_solver(rows_hints, cols_hints)
    ng_solver.run_solver()