async def refactoring_answer(answer: str) -> str:
    """
    Корректировка сообщение, если последний символ не является символом окончания предложения.
    :param answer: Исходное сообщение
    :return: Корректное сообщение
    """
    rev_answer = answer[::-1]
    for i_sym in rev_answer:
        if i_sym in '.?!':
            rev_index = rev_answer.find(i_sym)
            answer = answer[:len(answer) - rev_index]
            break
    return answer

