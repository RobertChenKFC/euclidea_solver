%lex
%%

\s+                /* skip whitespace */
[0-9]+("."[0.9]+)? return "NUMBER";
"+"                return "+";
"-"                return "-";
"*"                return "*";
"/"                return "/";
"^"                return "^";
"="                return "=";
"("                return "(";
")"                return ")";
","                return ",";
"sqrt"             return "sqrt";
"dist"             return "dist";
"angle"            return "angle";
[A-Za-z]+          return "IDENTIFIER";

/lex

%left "+" "-"
%left "*" "/"
%left "^"

%start condition

%%

condition
    : expr "=" expr { $$ = new EqNode($1, $3); return $$; }
    ;

expr
    : expr "+" expr        { $$ = new AddNode($1, $3); }
    | expr "-" expr        { $$ = new SubNode($1, $3); }
    | expr "*" expr        { $$ = new MulNode($1, $3); }
    | expr "/" expr        { $$ = new DivNode($1, $3); }
    | expr "^" expr        { $$ = new PowNode($1, $3); }
    | "(" expr ")"         { $$ = $2; }
    | "sqrt" "(" expr ")"  { $$ = new SqrtNode($3); }
    | "dist" "(" "IDENTIFIER" "," "IDENTIFIER" ")"  { $$ = new DistNode($3, $5); }
    | "angle" "(" "IDENTIFIER" "," "IDENTIFIER" "," "IDENTIFIER" ")" { $$ = new AngleNode($3, $5, $7);  }
    | "NUMBER" { $$ = new NumNode(parseFloat($1)); }
    ;
