from typing import Dict, List, Any
import chess
import time
from evaluate import evaluate_board, move_value, check_end_game
import chess.polyglot
debug_info: Dict[str, Any] = {}


MATE_SCORE = 100000000000
MATE_THRESHOLD =  99900000000

def load_opening_book():
    try:
        return chess.polyglot.open_reader("Human.bin")
    except Exception as e:
        print(f"Error loading opening book: {e}")
        return None


def get_opening_move(board: chess.Board, book_reader) -> chess.Move:
    try:
        entry = book_reader.find(board)
        if entry is not None:
            return entry.move
    except Exception as e:
        return None

def oppenings(board: chess.Board, debug=True) -> chess.Move:
    book_reader = load_opening_book()
    if book_reader is not None:
        opening_move = get_opening_move(board, book_reader)
        if opening_move is not None:
            return opening_move

def next_move(depth: int, board: chess.Board, debug=True) -> chess.Move:
    debug_info.clear()
    debug_info["nodes"] = 0
    t0 = time.time()

    book_reader = load_opening_book()
    opening_move = get_opening_move(board, book_reader)

    if opening_move is not None:
        debug_info["opening_found"] = True
        move = opening_move
    else:
        debug_info["opening_found"] = False
        move = minimax_root(depth, board)

    debug_info["time"] = time.time() - t0
    if debug:
        print(f"info {debug_info}")

    return move


def get_ordered_moves(board: chess.Board) -> List[chess.Move]:
    end_game = check_end_game(board)
    def orderer(move):
        return move_value(board, move, end_game)
    in_order = sorted(
        board.legal_moves, key=orderer, reverse=(board.turn == chess.WHITE)
    )
    return list(in_order)


def minimax_root(depth: int, board: chess.Board) -> chess.Move:

    maximize = board.turn == chess.WHITE
    best_move = -float("inf")
    if not maximize:
        best_move = float("inf")

    moves = get_ordered_moves(board)
    best_move_found = moves[0]

    for move in moves:
        board.push(move)

        if board.can_claim_draw():
            value = 0.0
        else:
            value = minimax(depth - 1, board, -float("inf"), float("inf"), not maximize)
        board.pop()
        if maximize and value >= best_move:
            best_move = value
            best_move_found = move
        elif not maximize and value <= best_move:
            best_move = value
            best_move_found = move

    return best_move_found


def minimax(
    depth: int,
    board: chess.Board,
    alpha: float,
    beta: float,
    is_maximising_player: bool,
) -> float:
    
    debug_info["nodes"] += 1

    if board.is_checkmate():
        return -MATE_SCORE if is_maximising_player else MATE_SCORE
    
    elif board.is_game_over():
        return 0

    if depth == 0:
        return evaluate_board(board)

    if is_maximising_player:
        best_move = -float("inf")
        moves = get_ordered_moves(board)
        for move in moves:
            board.push(move)
            curr_move = minimax(depth - 1, board, alpha, beta, not is_maximising_player)
            if curr_move > MATE_THRESHOLD:
                curr_move -= 1
            elif curr_move < -MATE_THRESHOLD:
                curr_move += 1
            best_move = max(
                best_move,
                curr_move,
            )
            board.pop()
            alpha = max(alpha, best_move)
            if beta <= alpha:
                return best_move
        return best_move
    else:
        best_move = float("inf")
        moves = get_ordered_moves(board)
        for move in moves:
            board.push(move)
            curr_move = minimax(depth - 1, board, alpha, beta, not is_maximising_player)
            if curr_move > MATE_THRESHOLD:
                curr_move -= 1
            elif curr_move < -MATE_THRESHOLD:
                curr_move += 1
            best_move = min(
                best_move,
                curr_move,
            )
            board.pop()
            beta = min(beta, best_move)
            if beta <= alpha:
                return best_move
        return best_move
