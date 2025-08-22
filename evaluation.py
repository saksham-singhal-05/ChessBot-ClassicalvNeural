import chess

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

def evaluate_material(board):
    white_material = 0
    black_material = 0
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_value = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                white_material += piece_value
            else:
                black_material += piece_value
    
    return white_material - black_material

def evaluate_check_safety(board):
    """Evaluate check situations - penalize unprotected checks"""
    check_score = 0
    
    if board.is_check():
        checking_side = not board.turn  
        king_square = board.king(board.turn)
        
        if king_square:
            attackers = board.attackers(checking_side, king_square)
            
            protected_attackers = 0
            unprotected_attackers = 0
            
            for attacker_square in attackers:
                defenders = board.attackers(checking_side, attacker_square)
                if len(defenders) > 1:  
                    protected_attackers += 1
                else:
                    unprotected_attackers += 1
            
            if checking_side == chess.WHITE:
                check_score += protected_attackers * 30
                check_score -= unprotected_attackers * 20
            else:
                check_score -= protected_attackers * 30
                check_score += unprotected_attackers * 20
    
    return check_score

def evaluate_position(board):
    material_score = evaluate_material(board)
    positional_score = 0
    
    center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
    for square in center_squares:
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color == chess.WHITE:
                positional_score += 10
            else:
                positional_score -= 10
    
    development_bonus = evaluate_development(board)
    positional_score += development_bonus
    
    check_bonus = evaluate_check_safety(board)
    positional_score += check_bonus
    
    king_safety = evaluate_king_safety(board)
    positional_score += king_safety
    
    return material_score + positional_score

def evaluate_development(board):
    development_score = 0
    
    if board.piece_at(chess.B1) != chess.Piece(chess.KNIGHT, chess.WHITE):
        development_score += 10
    if board.piece_at(chess.G1) != chess.Piece(chess.KNIGHT, chess.WHITE):
        development_score += 10
    if board.piece_at(chess.C1) != chess.Piece(chess.BISHOP, chess.WHITE):
        development_score += 10
    if board.piece_at(chess.F1) != chess.Piece(chess.BISHOP, chess.WHITE):
        development_score += 10
    
    if board.piece_at(chess.B8) != chess.Piece(chess.KNIGHT, chess.BLACK):
        development_score -= 10
    if board.piece_at(chess.G8) != chess.Piece(chess.KNIGHT, chess.BLACK):
        development_score -= 10
    if board.piece_at(chess.C8) != chess.Piece(chess.BISHOP, chess.BLACK):
        development_score -= 10
    if board.piece_at(chess.F8) != chess.Piece(chess.BISHOP, chess.BLACK):
        development_score -= 10
    
    return development_score

def evaluate_king_safety(board):
    """Evaluate king safety"""
    safety_score = 0
    
    white_king = board.king(chess.WHITE)
    black_king = board.king(chess.BLACK)
    
    if white_king:
        enemy_near_white = 0
        for square in chess.SQUARES:
            if chess.square_distance(square, white_king) <= 2:
                piece = board.piece_at(square)
                if piece and piece.color == chess.BLACK:
                    enemy_near_white += 1
        safety_score -= enemy_near_white * 5
    
    if black_king:
        enemy_near_black = 0
        for square in chess.SQUARES:
            if chess.square_distance(square, black_king) <= 2:
                piece = board.piece_at(square)
                if piece and piece.color == chess.WHITE:
                    enemy_near_black += 1
        safety_score += enemy_near_black * 5
    
    return safety_score
