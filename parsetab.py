
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'nonassocif_thenlet_precnonassocelsewhile_preclet_prec_assignrightassignleftandrightnotnonassoclowerlower_equalequalleftplusminuslefttimesdivrightuminusisnullrightpowleftdotand assign bool class colon comma div do dot else equal extends false if in int32 integer_literal isnull lbrace let lower lower_equal lpar minus new not object_identifier plus pow rbrace rpar semicolon string string_literal then times true type_identifier unit whileProgram : Class\n                   | Program ClassClass_body :\n                      | Class_body Field\n                      | Class_body MethodClass : class type_identifier lbrace Class_body rbrace\n                 | class type_identifier extends type_identifier lbrace Class_body rbraceClass : class type_identifier lbrace error rbrace\n                 | class type_identifier extends type_identifier lbrace error rbraceClass : class lbrace Class_body rbrace\n                 | class extends type_identifier lbrace Class_body rbraceClass : class object_identifier lbrace error rbrace\n                 | class object_identifier extends type_identifier lbrace Class_body rbraceClass : class type_identifier extends object_identifier lbrace Class_body rbraceField : object_identifier colon Type semicolon\n                 | object_identifier colon Type assign Expr semicolonField : object_identifier colon Type\n                 | object_identifier colon Type assign ExprField : object_identifier semicolon\n                 | object_identifier assign Expr semicolonMethod : object_identifier lpar Formals rpar colon Type BlockMethod : object_identifier lpar error rpar colon Type BlockType : type_identifier\n                | int32\n                | bool\n                | string\n                | unitFormals :\n                   | Formal\n                   | Formals comma FormalFormals : Formals FormalFormal : object_identifier colon TypeFormal : object_identifierBlock : lbrace Block_body rbraceBlock : lbrace error rbraceBlock : lbrace rbraceBlock : lbrace Block_body semicolon rbraceBlock_body : Expr\n                      | Block_body semicolon ExprBlock_body : Block_body ExprExpr : if Expr then Expr %prec if_then\n                | if Expr then Expr else ExprExpr : while Expr do Expr %prec while_precExpr : let object_identifier colon Type in Expr %prec let_prec\n                | let object_identifier colon Type assign Expr in Expr %prec let_prec_assignExpr : let object_identifier in Expr\n                | let object_identifier assign Expr in Expr Expr : object_identifier assign ExprExpr : minus Expr %prec uminusExpr : not Expr\n                | isnull ExprExpr : Expr and Expr\n                | Expr equal Expr\n                | Expr lower Expr\n                | Expr lower_equal Expr\n                | Expr plus Expr\n                | Expr minus Expr\n                | Expr times Expr\n                | Expr div Expr\n                | Expr pow ExprExpr : object_identifier lpar Args rpar\n                | Expr dot object_identifier lpar Args rparExpr : new type_identifierExpr : new object_identifierExpr : object_identifierExpr : LiteralExpr : lpar rparExpr : lpar Expr rparExpr : lpar error rparExpr : BlockArgs :\n                | Expr\n                | Args comma ExprLiteral : integer_literal\n                   | string_literal\n                   | Boolean_literalBoolean_literal : true\n                           | false'
    
_lr_action_items = {'class':([0,1,2,4,19,26,27,35,68,70,71,72,108,],[3,3,-1,-2,-10,-6,-8,-12,-11,-7,-9,-14,-13,]),'$end':([1,2,4,19,26,27,35,68,70,71,72,108,],[0,-1,-2,-10,-6,-8,-12,-11,-7,-9,-14,-13,]),'type_identifier':([3,7,10,14,30,55,103,125,135,137,],[5,12,17,25,41,97,41,41,41,41,]),'lbrace':([3,5,8,12,17,18,25,32,41,42,43,44,45,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,91,92,93,94,97,98,99,100,102,110,113,114,115,116,117,118,119,120,121,123,124,126,127,128,129,130,131,132,133,139,140,141,142,143,145,147,148,149,150,153,154,155,156,159,160,161,163,164,165,],[6,9,13,23,28,29,36,61,-23,-24,-25,-26,-27,-65,61,61,61,61,61,61,-66,-70,-74,-75,-76,61,-77,-78,61,61,61,61,61,61,61,61,61,61,61,61,-49,-50,-51,-67,-63,-64,61,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,61,61,61,61,-68,-69,-34,61,-40,-35,-61,61,61,-41,-43,-46,-37,-39,61,61,61,61,61,61,-62,-42,-44,-47,61,-45,]),'extends':([3,5,8,],[7,10,14,]),'object_identifier':([3,6,9,10,11,15,20,21,23,28,29,31,32,33,34,36,37,39,40,41,42,43,44,45,46,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,67,69,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,91,92,93,94,97,98,99,100,102,105,106,109,110,113,114,115,116,117,118,119,120,121,123,124,126,127,128,129,130,131,132,133,134,136,138,139,140,141,142,143,145,147,148,153,154,155,156,157,158,159,160,161,163,164,165,],[8,-3,-3,18,22,22,-4,-5,-3,-3,-3,-19,46,64,22,-3,22,22,-17,-23,-24,-25,-26,-27,-65,46,46,90,46,46,46,46,98,-66,-70,-74,-75,-76,46,-77,-78,-33,64,-29,22,-15,46,46,46,-20,46,46,46,46,46,46,46,46,46,122,-49,-50,-51,-67,-63,-64,46,-36,-38,64,-31,-18,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,46,46,46,46,-68,-69,-34,46,-40,-35,-32,-30,-16,-61,46,46,-41,-43,-46,-37,-39,46,46,46,46,-21,-22,-62,-42,-44,-47,46,-45,]),'rbrace':([6,9,11,15,16,20,21,23,24,28,29,31,34,36,37,38,39,40,41,42,43,44,45,46,56,57,58,59,60,61,62,63,69,73,77,91,92,93,94,97,98,99,100,101,102,109,110,113,114,115,116,117,118,119,120,121,128,129,130,131,132,133,138,139,142,143,145,147,148,157,158,159,160,161,163,165,],[-3,-3,19,26,27,-4,-5,-3,35,-3,-3,-19,68,-3,70,71,72,-17,-23,-24,-25,-26,-27,-65,-66,-70,-74,-75,-76,100,-77,-78,108,-15,-20,-49,-50,-51,-67,-63,-64,130,-36,133,-38,-18,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-68,-69,-34,147,-40,-35,-16,-61,-41,-43,-46,-37,-39,-21,-22,-62,-42,-44,-47,-45,]),'error':([9,13,28,33,54,61,],[16,24,38,66,96,101,]),'colon':([22,64,90,104,107,],[30,103,125,135,137,]),'semicolon':([22,40,41,42,43,44,45,46,47,56,57,58,59,60,62,63,91,92,93,94,97,98,99,100,102,109,110,113,114,115,116,117,118,119,120,121,128,129,130,132,133,139,142,143,145,147,148,159,160,161,163,165,],[31,73,-23,-24,-25,-26,-27,-65,77,-66,-70,-74,-75,-76,-77,-78,-49,-50,-51,-67,-63,-64,131,-36,-38,138,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-68,-69,-34,-40,-35,-61,-41,-43,-46,-37,-39,-62,-42,-44,-47,-45,]),'assign':([22,40,41,42,43,44,45,46,90,144,],[32,74,-23,-24,-25,-26,-27,75,127,155,]),'lpar':([22,32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,91,92,93,94,97,98,99,100,102,110,113,114,115,116,117,118,119,120,121,122,123,124,126,127,128,129,130,131,132,133,139,140,141,142,143,145,147,148,153,154,155,156,159,160,161,163,164,165,],[33,54,76,54,54,54,54,54,54,-66,-70,-74,-75,-76,54,-77,-78,54,54,54,54,54,54,54,54,54,54,54,54,-49,-50,-51,-67,-63,-64,54,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,141,54,54,54,54,-68,-69,-34,54,-40,-35,-61,54,54,-41,-43,-46,-37,-39,54,54,54,54,-62,-42,-44,-47,54,-45,]),'int32':([30,103,125,135,137,],[42,42,42,42,42,]),'bool':([30,103,125,135,137,],[43,43,43,43,43,]),'string':([30,103,125,135,137,],[44,44,44,44,44,]),'unit':([30,103,125,135,137,],[45,45,45,45,45,]),'if':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,91,92,93,94,97,98,99,100,102,110,113,114,115,116,117,118,119,120,121,123,124,126,127,128,129,130,131,132,133,139,140,141,142,143,145,147,148,153,154,155,156,159,160,161,163,164,165,],[48,-65,48,48,48,48,48,48,-66,-70,-74,-75,-76,48,-77,-78,48,48,48,48,48,48,48,48,48,48,48,48,-49,-50,-51,-67,-63,-64,48,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,48,48,48,48,-68,-69,-34,48,-40,-35,-61,48,48,-41,-43,-46,-37,-39,48,48,48,48,-62,-42,-44,-47,48,-45,]),'while':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,91,92,93,94,97,98,99,100,102,110,113,114,115,116,117,118,119,120,121,123,124,126,127,128,129,130,131,132,133,139,140,141,142,143,145,147,148,153,154,155,156,159,160,161,163,164,165,],[49,-65,49,49,49,49,49,49,-66,-70,-74,-75,-76,49,-77,-78,49,49,49,49,49,49,49,49,49,49,49,49,-49,-50,-51,-67,-63,-64,49,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,49,49,49,49,-68,-69,-34,49,-40,-35,-61,49,49,-41,-43,-46,-37,-39,49,49,49,49,-62,-42,-44,-47,49,-45,]),'let':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,91,92,93,94,97,98,99,100,102,110,113,114,115,116,117,118,119,120,121,123,124,126,127,128,129,130,131,132,133,139,140,141,142,143,145,147,148,153,154,155,156,159,160,161,163,164,165,],[50,-65,50,50,50,50,50,50,-66,-70,-74,-75,-76,50,-77,-78,50,50,50,50,50,50,50,50,50,50,50,50,-49,-50,-51,-67,-63,-64,50,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,50,50,50,50,-68,-69,-34,50,-40,-35,-61,50,50,-41,-43,-46,-37,-39,50,50,50,50,-62,-42,-44,-47,50,-45,]),'minus':([32,46,47,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,88,89,91,92,93,94,95,97,98,99,100,102,109,110,112,113,114,115,116,117,118,119,120,121,123,124,126,127,128,129,130,131,132,133,139,140,141,142,143,145,146,147,148,151,153,154,155,156,159,160,161,162,163,164,165,],[51,-65,83,51,51,51,51,51,51,-66,-70,-74,-75,-76,51,-77,-78,51,51,51,51,51,51,51,51,51,51,51,51,83,83,-49,83,-51,-67,83,-63,-64,51,-36,83,83,83,83,83,83,83,83,-56,-57,-58,-59,-60,51,51,51,51,-68,-69,-34,51,83,-35,-61,51,51,83,83,83,83,-37,83,83,51,51,51,51,-62,83,83,83,83,51,83,]),'not':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,91,92,93,94,97,98,99,100,102,110,113,114,115,116,117,118,119,120,121,123,124,126,127,128,129,130,131,132,133,139,140,141,142,143,145,147,148,153,154,155,156,159,160,161,163,164,165,],[52,-65,52,52,52,52,52,52,-66,-70,-74,-75,-76,52,-77,-78,52,52,52,52,52,52,52,52,52,52,52,52,-49,-50,-51,-67,-63,-64,52,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,52,52,52,52,-68,-69,-34,52,-40,-35,-61,52,52,-41,-43,-46,-37,-39,52,52,52,52,-62,-42,-44,-47,52,-45,]),'isnull':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,91,92,93,94,97,98,99,100,102,110,113,114,115,116,117,118,119,120,121,123,124,126,127,128,129,130,131,132,133,139,140,141,142,143,145,147,148,153,154,155,156,159,160,161,163,164,165,],[53,-65,53,53,53,53,53,53,-66,-70,-74,-75,-76,53,-77,-78,53,53,53,53,53,53,53,53,53,53,53,53,-49,-50,-51,-67,-63,-64,53,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,53,53,53,53,-68,-69,-34,53,-40,-35,-61,53,53,-41,-43,-46,-37,-39,53,53,53,53,-62,-42,-44,-47,53,-45,]),'new':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,91,92,93,94,97,98,99,100,102,110,113,114,115,116,117,118,119,120,121,123,124,126,127,128,129,130,131,132,133,139,140,141,142,143,145,147,148,153,154,155,156,159,160,161,163,164,165,],[55,-65,55,55,55,55,55,55,-66,-70,-74,-75,-76,55,-77,-78,55,55,55,55,55,55,55,55,55,55,55,55,-49,-50,-51,-67,-63,-64,55,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,55,55,55,55,-68,-69,-34,55,-40,-35,-61,55,55,-41,-43,-46,-37,-39,55,55,55,55,-62,-42,-44,-47,55,-45,]),'integer_literal':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,91,92,93,94,97,98,99,100,102,110,113,114,115,116,117,118,119,120,121,123,124,126,127,128,129,130,131,132,133,139,140,141,142,143,145,147,148,153,154,155,156,159,160,161,163,164,165,],[58,-65,58,58,58,58,58,58,-66,-70,-74,-75,-76,58,-77,-78,58,58,58,58,58,58,58,58,58,58,58,58,-49,-50,-51,-67,-63,-64,58,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,58,58,58,58,-68,-69,-34,58,-40,-35,-61,58,58,-41,-43,-46,-37,-39,58,58,58,58,-62,-42,-44,-47,58,-45,]),'string_literal':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,91,92,93,94,97,98,99,100,102,110,113,114,115,116,117,118,119,120,121,123,124,126,127,128,129,130,131,132,133,139,140,141,142,143,145,147,148,153,154,155,156,159,160,161,163,164,165,],[59,-65,59,59,59,59,59,59,-66,-70,-74,-75,-76,59,-77,-78,59,59,59,59,59,59,59,59,59,59,59,59,-49,-50,-51,-67,-63,-64,59,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,59,59,59,59,-68,-69,-34,59,-40,-35,-61,59,59,-41,-43,-46,-37,-39,59,59,59,59,-62,-42,-44,-47,59,-45,]),'true':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,91,92,93,94,97,98,99,100,102,110,113,114,115,116,117,118,119,120,121,123,124,126,127,128,129,130,131,132,133,139,140,141,142,143,145,147,148,153,154,155,156,159,160,161,163,164,165,],[62,-65,62,62,62,62,62,62,-66,-70,-74,-75,-76,62,-77,-78,62,62,62,62,62,62,62,62,62,62,62,62,-49,-50,-51,-67,-63,-64,62,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,62,62,62,62,-68,-69,-34,62,-40,-35,-61,62,62,-41,-43,-46,-37,-39,62,62,62,62,-62,-42,-44,-47,62,-45,]),'false':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,91,92,93,94,97,98,99,100,102,110,113,114,115,116,117,118,119,120,121,123,124,126,127,128,129,130,131,132,133,139,140,141,142,143,145,147,148,153,154,155,156,159,160,161,163,164,165,],[63,-65,63,63,63,63,63,63,-66,-70,-74,-75,-76,63,-77,-78,63,63,63,63,63,63,63,63,63,63,63,63,-49,-50,-51,-67,-63,-64,63,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,63,63,63,63,-68,-69,-34,63,-40,-35,-61,63,63,-41,-43,-46,-37,-39,63,63,63,63,-62,-42,-44,-47,63,-45,]),'rpar':([33,41,42,43,44,45,46,54,56,57,58,59,60,62,63,64,65,66,67,76,91,92,93,94,95,96,97,98,100,106,110,111,112,113,114,115,116,117,118,119,120,121,128,129,130,133,134,136,139,141,142,143,145,147,151,152,159,160,161,163,165,],[-28,-23,-24,-25,-26,-27,-65,94,-66,-70,-74,-75,-76,-77,-78,-33,104,107,-29,-71,-49,-50,-51,-67,128,129,-63,-64,-36,-31,-48,139,-72,-52,-53,-54,-55,-56,-57,-58,-59,-60,-68,-69,-34,-35,-32,-30,-61,-71,-41,-43,-46,-37,-73,159,-62,-42,-44,-47,-45,]),'comma':([33,41,42,43,44,45,46,56,57,58,59,60,62,63,64,65,67,76,91,92,93,94,97,98,100,106,110,111,112,113,114,115,116,117,118,119,120,121,128,129,130,133,134,136,139,141,142,143,145,147,151,152,159,160,161,163,165,],[-28,-23,-24,-25,-26,-27,-65,-66,-70,-74,-75,-76,-77,-78,-33,105,-29,-71,-49,-50,-51,-67,-63,-64,-36,-31,-48,140,-72,-52,-53,-54,-55,-56,-57,-58,-59,-60,-68,-69,-34,-35,-32,-30,-61,-71,-41,-43,-46,-37,-73,140,-62,-42,-44,-47,-45,]),'in':([41,42,43,44,45,46,56,57,58,59,60,62,63,90,91,92,93,94,97,98,100,110,113,114,115,116,117,118,119,120,121,128,129,130,133,139,142,143,144,145,146,147,159,160,161,162,163,165,],[-23,-24,-25,-26,-27,-65,-66,-70,-74,-75,-76,-77,-78,126,-49,-50,-51,-67,-63,-64,-36,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-68,-69,-34,-35,-61,-41,-43,154,-46,156,-37,-62,-42,-44,164,-47,-45,]),'and':([46,47,56,57,58,59,60,62,63,88,89,91,92,93,94,95,97,98,100,102,109,110,112,113,114,115,116,117,118,119,120,121,128,129,130,132,133,139,142,143,145,146,147,148,151,159,160,161,162,163,165,],[-65,78,-66,-70,-74,-75,-76,-77,-78,78,78,-49,-50,-51,-67,78,-63,-64,-36,78,78,78,78,-52,-53,-54,-55,-56,-57,-58,-59,-60,-68,-69,-34,78,-35,-61,78,78,78,78,-37,78,78,-62,78,78,78,78,78,]),'equal':([46,47,56,57,58,59,60,62,63,88,89,91,92,93,94,95,97,98,100,102,109,110,112,113,114,115,116,117,118,119,120,121,128,129,130,132,133,139,142,143,145,146,147,148,151,159,160,161,162,163,165,],[-65,79,-66,-70,-74,-75,-76,-77,-78,79,79,-49,79,-51,-67,79,-63,-64,-36,79,79,79,79,79,None,None,None,-56,-57,-58,-59,-60,-68,-69,-34,79,-35,-61,79,79,79,79,-37,79,79,-62,79,79,79,79,79,]),'lower':([46,47,56,57,58,59,60,62,63,88,89,91,92,93,94,95,97,98,100,102,109,110,112,113,114,115,116,117,118,119,120,121,128,129,130,132,133,139,142,143,145,146,147,148,151,159,160,161,162,163,165,],[-65,80,-66,-70,-74,-75,-76,-77,-78,80,80,-49,80,-51,-67,80,-63,-64,-36,80,80,80,80,80,None,None,None,-56,-57,-58,-59,-60,-68,-69,-34,80,-35,-61,80,80,80,80,-37,80,80,-62,80,80,80,80,80,]),'lower_equal':([46,47,56,57,58,59,60,62,63,88,89,91,92,93,94,95,97,98,100,102,109,110,112,113,114,115,116,117,118,119,120,121,128,129,130,132,133,139,142,143,145,146,147,148,151,159,160,161,162,163,165,],[-65,81,-66,-70,-74,-75,-76,-77,-78,81,81,-49,81,-51,-67,81,-63,-64,-36,81,81,81,81,81,None,None,None,-56,-57,-58,-59,-60,-68,-69,-34,81,-35,-61,81,81,81,81,-37,81,81,-62,81,81,81,81,81,]),'plus':([46,47,56,57,58,59,60,62,63,88,89,91,92,93,94,95,97,98,100,102,109,110,112,113,114,115,116,117,118,119,120,121,128,129,130,132,133,139,142,143,145,146,147,148,151,159,160,161,162,163,165,],[-65,82,-66,-70,-74,-75,-76,-77,-78,82,82,-49,82,-51,-67,82,-63,-64,-36,82,82,82,82,82,82,82,82,-56,-57,-58,-59,-60,-68,-69,-34,82,-35,-61,82,82,82,82,-37,82,82,-62,82,82,82,82,82,]),'times':([46,47,56,57,58,59,60,62,63,88,89,91,92,93,94,95,97,98,100,102,109,110,112,113,114,115,116,117,118,119,120,121,128,129,130,132,133,139,142,143,145,146,147,148,151,159,160,161,162,163,165,],[-65,84,-66,-70,-74,-75,-76,-77,-78,84,84,-49,84,-51,-67,84,-63,-64,-36,84,84,84,84,84,84,84,84,84,84,-58,-59,-60,-68,-69,-34,84,-35,-61,84,84,84,84,-37,84,84,-62,84,84,84,84,84,]),'div':([46,47,56,57,58,59,60,62,63,88,89,91,92,93,94,95,97,98,100,102,109,110,112,113,114,115,116,117,118,119,120,121,128,129,130,132,133,139,142,143,145,146,147,148,151,159,160,161,162,163,165,],[-65,85,-66,-70,-74,-75,-76,-77,-78,85,85,-49,85,-51,-67,85,-63,-64,-36,85,85,85,85,85,85,85,85,85,85,-58,-59,-60,-68,-69,-34,85,-35,-61,85,85,85,85,-37,85,85,-62,85,85,85,85,85,]),'pow':([46,47,56,57,58,59,60,62,63,88,89,91,92,93,94,95,97,98,100,102,109,110,112,113,114,115,116,117,118,119,120,121,128,129,130,132,133,139,142,143,145,146,147,148,151,159,160,161,162,163,165,],[-65,86,-66,-70,-74,-75,-76,-77,-78,86,86,86,86,86,-67,86,-63,-64,-36,86,86,86,86,86,86,86,86,86,86,86,86,86,-68,-69,-34,86,-35,-61,86,86,86,86,-37,86,86,-62,86,86,86,86,86,]),'dot':([46,47,56,57,58,59,60,62,63,88,89,91,92,93,94,95,97,98,100,102,109,110,112,113,114,115,116,117,118,119,120,121,128,129,130,132,133,139,142,143,145,146,147,148,151,159,160,161,162,163,165,],[-65,87,-66,-70,-74,-75,-76,-77,-78,87,87,87,87,87,-67,87,-63,-64,-36,87,87,87,87,87,87,87,87,87,87,87,87,87,-68,-69,-34,87,-35,-61,87,87,87,87,-37,87,87,-62,87,87,87,87,87,]),'then':([46,56,57,58,59,60,62,63,88,91,92,93,94,97,98,100,110,113,114,115,116,117,118,119,120,121,128,129,130,133,139,142,143,145,147,159,160,161,163,165,],[-65,-66,-70,-74,-75,-76,-77,-78,123,-49,-50,-51,-67,-63,-64,-36,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-68,-69,-34,-35,-61,-41,-43,-46,-37,-62,-42,-44,-47,-45,]),'do':([46,56,57,58,59,60,62,63,89,91,92,93,94,97,98,100,110,113,114,115,116,117,118,119,120,121,128,129,130,133,139,142,143,145,147,159,160,161,163,165,],[-65,-66,-70,-74,-75,-76,-77,-78,124,-49,-50,-51,-67,-63,-64,-36,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-68,-69,-34,-35,-61,-41,-43,-46,-37,-62,-42,-44,-47,-45,]),'else':([46,56,57,58,59,60,62,63,91,92,93,94,97,98,100,110,113,114,115,116,117,118,119,120,121,128,129,130,133,139,142,143,145,147,159,160,161,163,165,],[-65,-66,-70,-74,-75,-76,-77,-78,-49,-50,-51,-67,-63,-64,-36,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-68,-69,-34,-35,-61,153,-43,-46,-37,-62,-42,-44,-47,-45,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'Program':([0,],[1,]),'Class':([0,1,],[2,4,]),'Class_body':([6,9,23,28,29,36,],[11,15,34,37,39,69,]),'Field':([11,15,34,37,39,69,],[20,20,20,20,20,20,]),'Method':([11,15,34,37,39,69,],[21,21,21,21,21,21,]),'Type':([30,103,125,135,137,],[40,134,144,149,150,]),'Expr':([32,48,49,51,52,53,54,61,74,75,76,78,79,80,81,82,83,84,85,86,99,123,124,126,127,131,140,141,153,154,155,156,164,],[47,88,89,91,92,93,95,102,109,110,112,113,114,115,116,117,118,119,120,121,132,142,143,145,146,148,151,112,160,161,162,163,165,]),'Literal':([32,48,49,51,52,53,54,61,74,75,76,78,79,80,81,82,83,84,85,86,99,123,124,126,127,131,140,141,153,154,155,156,164,],[56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,]),'Block':([32,48,49,51,52,53,54,61,74,75,76,78,79,80,81,82,83,84,85,86,99,123,124,126,127,131,140,141,149,150,153,154,155,156,164,],[57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,157,158,57,57,57,57,57,]),'Boolean_literal':([32,48,49,51,52,53,54,61,74,75,76,78,79,80,81,82,83,84,85,86,99,123,124,126,127,131,140,141,153,154,155,156,164,],[60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,]),'Formals':([33,],[65,]),'Formal':([33,65,105,],[67,106,136,]),'Block_body':([61,],[99,]),'Args':([76,141,],[111,152,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> Program","S'",1,None,None,None),
  ('Program -> Class','Program',1,'p_Program','myParser.py',48),
  ('Program -> Program Class','Program',2,'p_Program','myParser.py',49),
  ('Class_body -> <empty>','Class_body',0,'p_Class_body','myParser.py',58),
  ('Class_body -> Class_body Field','Class_body',2,'p_Class_body','myParser.py',59),
  ('Class_body -> Class_body Method','Class_body',2,'p_Class_body','myParser.py',60),
  ('Class -> class type_identifier lbrace Class_body rbrace','Class',5,'p_Class','myParser.py',71),
  ('Class -> class type_identifier extends type_identifier lbrace Class_body rbrace','Class',7,'p_Class','myParser.py',72),
  ('Class -> class type_identifier lbrace error rbrace','Class',5,'p_Class_error','myParser.py',88),
  ('Class -> class type_identifier extends type_identifier lbrace error rbrace','Class',7,'p_Class_error','myParser.py',89),
  ('Class -> class lbrace Class_body rbrace','Class',4,'p_Class_error_no_name','myParser.py',96),
  ('Class -> class extends type_identifier lbrace Class_body rbrace','Class',6,'p_Class_error_no_name','myParser.py',97),
  ('Class -> class object_identifier lbrace error rbrace','Class',5,'p_Class_error_object_id_name','myParser.py',106),
  ('Class -> class object_identifier extends type_identifier lbrace Class_body rbrace','Class',7,'p_Class_error_object_id_name','myParser.py',107),
  ('Class -> class type_identifier extends object_identifier lbrace Class_body rbrace','Class',7,'p_Class_error_object_id_name_parent','myParser.py',116),
  ('Field -> object_identifier colon Type semicolon','Field',4,'p_Field','myParser.py',124),
  ('Field -> object_identifier colon Type assign Expr semicolon','Field',6,'p_Field','myParser.py',125),
  ('Field -> object_identifier colon Type','Field',3,'p_Field_error_semicolon','myParser.py',136),
  ('Field -> object_identifier colon Type assign Expr','Field',5,'p_Field_error_semicolon','myParser.py',137),
  ('Field -> object_identifier semicolon','Field',2,'p_Field_error_type','myParser.py',151),
  ('Field -> object_identifier assign Expr semicolon','Field',4,'p_Field_error_type','myParser.py',152),
  ('Method -> object_identifier lpar Formals rpar colon Type Block','Method',7,'p_Method','myParser.py',165),
  ('Method -> object_identifier lpar error rpar colon Type Block','Method',7,'p_Method_error','myParser.py',171),
  ('Type -> type_identifier','Type',1,'p_Type','myParser.py',179),
  ('Type -> int32','Type',1,'p_Type','myParser.py',180),
  ('Type -> bool','Type',1,'p_Type','myParser.py',181),
  ('Type -> string','Type',1,'p_Type','myParser.py',182),
  ('Type -> unit','Type',1,'p_Type','myParser.py',183),
  ('Formals -> <empty>','Formals',0,'p_Formals','myParser.py',188),
  ('Formals -> Formal','Formals',1,'p_Formals','myParser.py',189),
  ('Formals -> Formals comma Formal','Formals',3,'p_Formals','myParser.py',190),
  ('Formals -> Formals Formal','Formals',2,'p_Formals_error_comma','myParser.py',205),
  ('Formal -> object_identifier colon Type','Formal',3,'p_Formal','myParser.py',213),
  ('Formal -> object_identifier','Formal',1,'p_Formals_error_type','myParser.py',219),
  ('Block -> lbrace Block_body rbrace','Block',3,'p_Block','myParser.py',227),
  ('Block -> lbrace error rbrace','Block',3,'p_Block_error','myParser.py',232),
  ('Block -> lbrace rbrace','Block',2,'p_Block_error_empty','myParser.py',241),
  ('Block -> lbrace Block_body semicolon rbrace','Block',4,'p_Block_error_end_semicolon','myParser.py',250),
  ('Block_body -> Expr','Block_body',1,'p_Block_body','myParser.py',257),
  ('Block_body -> Block_body semicolon Expr','Block_body',3,'p_Block_body','myParser.py',258),
  ('Block_body -> Block_body Expr','Block_body',2,'p_Block_body_error_expr_semicolon','myParser.py',270),
  ('Expr -> if Expr then Expr','Expr',4,'p_Expr_If_then','myParser.py',278),
  ('Expr -> if Expr then Expr else Expr','Expr',6,'p_Expr_If_then','myParser.py',279),
  ('Expr -> while Expr do Expr','Expr',4,'p_Expr_while','myParser.py',289),
  ('Expr -> let object_identifier colon Type in Expr','Expr',6,'p_Expr_let','myParser.py',294),
  ('Expr -> let object_identifier colon Type assign Expr in Expr','Expr',8,'p_Expr_let','myParser.py',295),
  ('Expr -> let object_identifier in Expr','Expr',4,'p_Expr_let_error_type','myParser.py',306),
  ('Expr -> let object_identifier assign Expr in Expr','Expr',6,'p_Expr_let_error_type','myParser.py',307),
  ('Expr -> object_identifier assign Expr','Expr',3,'p_Expr_assign','myParser.py',320),
  ('Expr -> minus Expr','Expr',2,'p_Expr_uminus','myParser.py',325),
  ('Expr -> not Expr','Expr',2,'p_Expr_UnOp','myParser.py',330),
  ('Expr -> isnull Expr','Expr',2,'p_Expr_UnOp','myParser.py',331),
  ('Expr -> Expr and Expr','Expr',3,'p_Expr_BinOp','myParser.py',336),
  ('Expr -> Expr equal Expr','Expr',3,'p_Expr_BinOp','myParser.py',337),
  ('Expr -> Expr lower Expr','Expr',3,'p_Expr_BinOp','myParser.py',338),
  ('Expr -> Expr lower_equal Expr','Expr',3,'p_Expr_BinOp','myParser.py',339),
  ('Expr -> Expr plus Expr','Expr',3,'p_Expr_BinOp','myParser.py',340),
  ('Expr -> Expr minus Expr','Expr',3,'p_Expr_BinOp','myParser.py',341),
  ('Expr -> Expr times Expr','Expr',3,'p_Expr_BinOp','myParser.py',342),
  ('Expr -> Expr div Expr','Expr',3,'p_Expr_BinOp','myParser.py',343),
  ('Expr -> Expr pow Expr','Expr',3,'p_Expr_BinOp','myParser.py',344),
  ('Expr -> object_identifier lpar Args rpar','Expr',4,'p_Expr_Call','myParser.py',350),
  ('Expr -> Expr dot object_identifier lpar Args rpar','Expr',6,'p_Expr_Call','myParser.py',351),
  ('Expr -> new type_identifier','Expr',2,'p_Expr_New','myParser.py',362),
  ('Expr -> new object_identifier','Expr',2,'p_Expr_New_error_obj_id','myParser.py',368),
  ('Expr -> object_identifier','Expr',1,'p_Expr_Object_id','myParser.py',376),
  ('Expr -> Literal','Expr',1,'p_Expr_literal','myParser.py',381),
  ('Expr -> lpar rpar','Expr',2,'p_Expr_Unit','myParser.py',386),
  ('Expr -> lpar Expr rpar','Expr',3,'p_Expr_Par_expr','myParser.py',391),
  ('Expr -> lpar error rpar','Expr',3,'p_Expr_Par_expr_error','myParser.py',397),
  ('Expr -> Block','Expr',1,'p_Expr_block','myParser.py',405),
  ('Args -> <empty>','Args',0,'p_Args','myParser.py',410),
  ('Args -> Expr','Args',1,'p_Args','myParser.py',411),
  ('Args -> Args comma Expr','Args',3,'p_Args','myParser.py',412),
  ('Literal -> integer_literal','Literal',1,'p_Literal','myParser.py',425),
  ('Literal -> string_literal','Literal',1,'p_Literal','myParser.py',426),
  ('Literal -> Boolean_literal','Literal',1,'p_Literal','myParser.py',427),
  ('Boolean_literal -> true','Boolean_literal',1,'p_Boolean_literal','myParser.py',435),
  ('Boolean_literal -> false','Boolean_literal',1,'p_Boolean_literal','myParser.py',436),
]
