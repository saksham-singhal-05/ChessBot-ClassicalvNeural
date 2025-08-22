import chess
from evaluation import evaluate_position

def minimax_search(board, depth, alpha, beta, maximizing_player):
    """
    Minimax with alpha-beta pruning for efficient search
    maximizing_player: True if current player should maximize, False if minimize
    """
    if depth == 0 or board.is_game_over():
        return evaluate_position(board), None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in order_moves(board):
            board.push(move)
            eval_score, _ = minimax_search(board, depth - 1, alpha, beta, False)
            board.pop()

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Alpha-beta cutoff

        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in order_moves(board):
            board.push(move)
            eval_score, _ = minimax_search(board, depth - 1, alpha, beta, True)
            board.pop()

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha-beta cutoff

        return min_eval, best_move

def order_moves(board):
    """Order moves for better alpha-beta pruning efficiency"""
    moves = list(board.legal_moves)
    
    # Separate move types for better ordering
    captures = []
    protected_checks = []
    unprotected_checks = []
    promotions = []
    other_moves = []

    for move in moves:
        # Promotions get highest priority
        if move.promotion:
            promotions.append(move)
        # Captures get high priority
        elif board.is_capture(move):
            captures.append(move)
        # Separate protected and unprotected checks
        elif board.gives_check(move):
            board.push(move)
            if is_protected_check(board, move):
                protected_checks.append(move)
            else:
                unprotected_checks.append(move)
            board.pop()
        else:
            other_moves.append(move)

    # Return in order: promotions, captures, protected checks, other moves, unprotected checks last
    return promotions + captures + protected_checks + other_moves + unprotected_checks

def is_protected_check(board, checking_move):
    """Check if the piece giving check is protected"""
    if not board.is_check():
        return False
    
    # Find the piece that just moved (giving check)
    checking_piece_square = checking_move.to_square
    checking_side = not board.turn  # The side that just moved
    
    # Count defenders of the checking piece
    defenders = board.attackers(checking_side, checking_piece_square)
    
    # If there are defenders (other than the piece itself), it's protected
    return len(defenders) > 0
