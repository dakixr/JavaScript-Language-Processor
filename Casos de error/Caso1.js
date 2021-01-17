// Multitud de errores semánticos

function number Factorial (number n)	
{
	if (n < 0)	return 1;
	return n + Factorial (n + 1);	
}

num = 45;

Factorial(num, 'Este argumento sobra');
Factorial(num);

let string s;

s = 4 > 6;
s %= 5;

if (s){
	alert(s);
}


function number Factorial2 (number n)	
{
	if (n < 0){
		return 9;
	}

	return 'return';
}


