replace_nth(N, OldElem, NewElem, List, List2) :-
    length(L1, N),
    append(L1, [OldElem|Rest], List),
    append(L1, [NewElem|Rest], List2).

replace_m_n(Matrix, I, J, NewValue, NewMatrix) :-
    replace_nth(I, Old1, New1, Matrix, NewMatrix),
    replace_nth(J, _OldElem2, NewValue, Old1, New1).

empty(x).

nth0_2(Row, Column, List, Element) :-
    nth0(Row, List, SubList),
    nth0(Column, SubList, Element).

isValid(Element1 , Element2):-
    empty(Element1) , empty(Element2).

checkColumn(Columns , Rows , NewRows ):-
    Columns = 0  , NewRows is Rows + 1  , ! ; NewRows is Rows.

columnsValid(Rows , Columns , _ , SColumn , NewRows , NewColumns):-
    NewColumns is Columns mod SColumn,
    checkColumn(NewColumns , Rows , NewRows).

isGoal(Rows , Columns , SRow , SColumn , N):-
    TestRow is SRow -1,
    TestColumn is SColumn -1,
    Rows = TestRow ,
    Columns =TestColumn,
    N >= 1.

searchStopper(Rows , Columns , SRow , SColumn):-
    TestRow is SRow -1,
    TestColumn is SColumn -1,
    Rows =< TestRow ,
    Columns =< TestColumn.

search(Rows , Columns , SRow , SColumn , Board , N , Solution ):-
    isGoal(Rows , Columns , SRow , SColumn , N) , ! 
    , Solution = Board.

% Cut Operator is Missing 
search(Rows , Columns , SRow , SColumn , Board , N , Solution):-
    NewColumns is Columns +1,
    nth0_2(Rows , Columns , Board , Element1),
    nth0_2(Rows , NewColumns , Board , Element2),
    isValid(Element1,  Element2),
    replace_m_n(Board , Rows , Columns , domino , NvList) ,
    replace_m_n(NvList , Rows , NewColumns , domino , NvList2) ,
    N2 is N +1,
    columnsValid(Rows , NewColumns ,SRow , SColumn , NR , NC ),
    search(NR , NC , SRow , SColumn , NvList2 , N2 , Solution).


% Cut Operator is Missing 
search(Rows , Columns , SRow , SColumn , Board, N , Solution):-
    NewRows is Rows + 1,
    nth0_2(Rows , Columns , Board , Element1),
    nth0_2(NewRows , Columns , Board , Element2),
    isValid(Element1,  Element2),
    replace_m_n(Board , Rows , Columns , domino , NvList) ,
    replace_m_n(NvList , NewRows , Columns , domino , NvList2) ,
    N2 is N +1,
    NewColumns is Columns +1 ,
    columnsValid(Rows , NewColumns ,SRow , SColumn , NR , NC ),
    search(NR , NC , SRow , SColumn , NvList2 , N2 , Solution).


search(Rows , Columns , SRow , SColumn , Board , N , Solution):-
    NewColumns is Columns +1 ,
    columnsValid(Rows , NewColumns ,SRow , SColumn , NR , NC ),
    searchStopper(NR , NC , SRow , SColumn),
    search(NR , NC , SRow , SColumn , Board , N , Solution).

initSearch(Rows , Columns , Board , Solution):-
    search( 0, 0 ,Rows , Columns , Board , 0 , Solution).
