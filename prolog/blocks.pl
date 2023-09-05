
:-
    assert(block(cylinder)),
    assert(block(prism)),
    assert(block(sphere)),
    assert(color(cylinder, red)),
    assert(color(prism, white)),
    assert(color(sphere, black)),
    assert(upon(desk1, cylinder)),
    assert(upon(desk2, prism)),
    assert(upon(desk2, sphere)).

black_object(X) :- block(X), color(X, black).

free_desk(Desk) :- \+upon(Desk, _).

take_from_desk(Desk, Obj) :-
	block(Obj),
	upon(Desk, Obj),
        % drive_arm(....),
	retract(upon(Desk, Obj)),
	assert(held(Obj)).

%take_from_desk(Desk) :- upon(Desk, X), retract(upon(Desk, X)), ! .

