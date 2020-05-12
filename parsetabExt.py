
# parsetabExt.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'nonassocif_thenlet_precnonassocelsewhile_preclet_prec_assignrightassignleftandorxorrightnotnonassoclowerlargerlower_equallarger_equalequalleftplusminuslefttimesdivmodulorightuminusisnullrightpowleftdotand assign bool class colon comma div do dot else equal extends false if in int32 integer_literal isnull larger larger_equal lbrace let lower lower_equal lpar minus modulo new not object_identifier or plus pow rbrace rpar semicolon string string_literal then times true type_identifier unit while xorProgram : Class\n                   | Program ClassClass_body :\n                      | Class_body Field\n                      | Class_body MethodClass : class type_identifier lbrace Class_body rbrace\n                 | class type_identifier extends type_identifier lbrace Class_body rbraceClass : class type_identifier lbrace error rbrace\n                 | class type_identifier extends type_identifier lbrace error rbraceClass : class lbrace Class_body rbrace\n                 | class extends type_identifier lbrace Class_body rbraceClass : class object_identifier lbrace error rbrace\n                 | class object_identifier extends type_identifier lbrace Class_body rbraceClass : class type_identifier extends object_identifier lbrace Class_body rbraceField : object_identifier colon Type semicolon\n                 | object_identifier colon Type assign Expr semicolonField : object_identifier colon Type\n                 | object_identifier colon Type assign ExprField : object_identifier semicolon\n                 | object_identifier assign Expr semicolonMethod : object_identifier lpar Formals rpar colon Type BlockMethod : object_identifier lpar error rpar colon Type BlockType : type_identifier\n                | int32\n                | bool\n                | string\n                | unitFormals :\n                   | Formal\n                   | Formals comma FormalFormals : Formals FormalFormal : object_identifier colon TypeFormal : object_identifierBlock : lbrace Block_body rbraceBlock : lbrace error rbraceBlock : lbrace rbraceBlock : lbrace Block_body semicolon rbraceBlock_body : Expr\n                      | Block_body semicolon ExprBlock_body : Block_body ExprExpr : if Expr then Expr %prec if_then\n                | if Expr then Expr else ExprExpr : while Expr do Expr %prec while_precExpr : let object_identifier colon Type in Expr %prec let_prec\n                | let object_identifier colon Type assign Expr in Expr %prec let_prec_assignExpr : let object_identifier in Expr\n                | let object_identifier assign Expr in Expr Expr : object_identifier assign ExprExpr : minus Expr %prec uminusExpr : not Expr\n                | isnull ExprExpr : Expr and Expr\n                | Expr or Expr\n                | Expr xor Expr\n                | Expr equal Expr\n                | Expr lower Expr\n                | Expr larger Expr\n                | Expr lower_equal Expr\n                | Expr larger_equal Expr\n                | Expr plus Expr\n                | Expr minus Expr\n                | Expr times Expr\n                | Expr div Expr\n                | Expr modulo Expr\n                | Expr pow ExprExpr : object_identifier lpar Args rpar\n                | Expr dot object_identifier lpar Args rparExpr : new type_identifierExpr : new object_identifierExpr : object_identifierExpr : LiteralExpr : lpar rparExpr : lpar Expr rparExpr : lpar error rparExpr : BlockArgs :\n                | Expr\n                | Args comma ExprLiteral : integer_literal\n                   | string_literal\n                   | Boolean_literalBoolean_literal : true\n                           | false'
    
_lr_action_items = {'class':([0,1,2,4,19,26,27,35,68,70,71,72,113,],[3,3,-1,-2,-10,-6,-8,-12,-11,-7,-9,-14,-13,]),'$end':([1,2,4,19,26,27,35,68,70,71,72,113,],[0,-1,-2,-10,-6,-8,-12,-11,-7,-9,-14,-13,]),'type_identifier':([3,7,10,14,30,55,108,135,145,147,],[5,12,17,25,41,102,41,41,41,41,]),'lbrace':([3,5,8,12,17,18,25,32,41,42,43,44,45,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,96,97,98,99,102,103,104,105,107,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,133,134,136,137,138,139,140,141,142,143,149,150,151,152,153,155,157,158,159,160,163,164,165,166,169,170,171,173,174,175,],[6,9,13,23,28,29,36,61,-23,-24,-25,-26,-27,-70,61,61,61,61,61,61,-71,-75,-79,-80,-81,61,-82,-83,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,-49,-50,-51,-72,-68,-69,61,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,61,61,61,61,-73,-74,-34,61,-40,-35,-66,61,61,-41,-43,-46,-37,-39,61,61,61,61,61,61,-67,-42,-44,-47,61,-45,]),'extends':([3,5,8,],[7,10,14,]),'object_identifier':([3,6,9,10,11,15,20,21,23,28,29,31,32,33,34,36,37,39,40,41,42,43,44,45,46,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,67,69,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,96,97,98,99,102,103,104,105,107,110,111,114,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,133,134,136,137,138,139,140,141,142,143,144,146,148,149,150,151,152,153,155,157,158,163,164,165,166,167,168,169,170,171,173,174,175,],[8,-3,-3,18,22,22,-4,-5,-3,-3,-3,-19,46,64,22,-3,22,22,-17,-23,-24,-25,-26,-27,-70,46,46,95,46,46,46,46,103,-71,-75,-79,-80,-81,46,-82,-83,-33,64,-29,22,-15,46,46,46,-20,46,46,46,46,46,46,46,46,46,46,46,46,46,46,132,-49,-50,-51,-72,-68,-69,46,-36,-38,64,-31,-18,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,46,46,46,46,-73,-74,-34,46,-40,-35,-32,-30,-16,-66,46,46,-41,-43,-46,-37,-39,46,46,46,46,-21,-22,-67,-42,-44,-47,46,-45,]),'rbrace':([6,9,11,15,16,20,21,23,24,28,29,31,34,36,37,38,39,40,41,42,43,44,45,46,56,57,58,59,60,61,62,63,69,73,77,96,97,98,99,102,103,104,105,106,107,114,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,141,142,143,148,149,152,153,155,157,158,167,168,169,170,171,173,175,],[-3,-3,19,26,27,-4,-5,-3,35,-3,-3,-19,68,-3,70,71,72,-17,-23,-24,-25,-26,-27,-70,-71,-75,-79,-80,-81,105,-82,-83,113,-15,-20,-49,-50,-51,-72,-68,-69,140,-36,143,-38,-18,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,-73,-74,-34,157,-40,-35,-16,-66,-41,-43,-46,-37,-39,-21,-22,-67,-42,-44,-47,-45,]),'error':([9,13,28,33,54,61,],[16,24,38,66,101,106,]),'colon':([22,64,95,109,112,],[30,108,135,145,147,]),'semicolon':([22,40,41,42,43,44,45,46,47,56,57,58,59,60,62,63,96,97,98,99,102,103,104,105,107,114,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,142,143,149,152,153,155,157,158,169,170,171,173,175,],[31,73,-23,-24,-25,-26,-27,-70,77,-71,-75,-79,-80,-81,-82,-83,-49,-50,-51,-72,-68,-69,141,-36,-38,148,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,-73,-74,-34,-40,-35,-66,-41,-43,-46,-37,-39,-67,-42,-44,-47,-45,]),'assign':([22,40,41,42,43,44,45,46,95,154,],[32,74,-23,-24,-25,-26,-27,75,137,165,]),'lpar':([22,32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,96,97,98,99,102,103,104,105,107,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,136,137,138,139,140,141,142,143,149,150,151,152,153,155,157,158,163,164,165,166,169,170,171,173,174,175,],[33,54,76,54,54,54,54,54,54,-71,-75,-79,-80,-81,54,-82,-83,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,-49,-50,-51,-72,-68,-69,54,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,151,54,54,54,54,-73,-74,-34,54,-40,-35,-66,54,54,-41,-43,-46,-37,-39,54,54,54,54,-67,-42,-44,-47,54,-45,]),'int32':([30,108,135,145,147,],[42,42,42,42,42,]),'bool':([30,108,135,145,147,],[43,43,43,43,43,]),'string':([30,108,135,145,147,],[44,44,44,44,44,]),'unit':([30,108,135,145,147,],[45,45,45,45,45,]),'if':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,96,97,98,99,102,103,104,105,107,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,133,134,136,137,138,139,140,141,142,143,149,150,151,152,153,155,157,158,163,164,165,166,169,170,171,173,174,175,],[48,-70,48,48,48,48,48,48,-71,-75,-79,-80,-81,48,-82,-83,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,-49,-50,-51,-72,-68,-69,48,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,48,48,48,48,-73,-74,-34,48,-40,-35,-66,48,48,-41,-43,-46,-37,-39,48,48,48,48,-67,-42,-44,-47,48,-45,]),'while':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,96,97,98,99,102,103,104,105,107,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,133,134,136,137,138,139,140,141,142,143,149,150,151,152,153,155,157,158,163,164,165,166,169,170,171,173,174,175,],[49,-70,49,49,49,49,49,49,-71,-75,-79,-80,-81,49,-82,-83,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,-49,-50,-51,-72,-68,-69,49,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,49,49,49,49,-73,-74,-34,49,-40,-35,-66,49,49,-41,-43,-46,-37,-39,49,49,49,49,-67,-42,-44,-47,49,-45,]),'let':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,96,97,98,99,102,103,104,105,107,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,133,134,136,137,138,139,140,141,142,143,149,150,151,152,153,155,157,158,163,164,165,166,169,170,171,173,174,175,],[50,-70,50,50,50,50,50,50,-71,-75,-79,-80,-81,50,-82,-83,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,-49,-50,-51,-72,-68,-69,50,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,50,50,50,50,-73,-74,-34,50,-40,-35,-66,50,50,-41,-43,-46,-37,-39,50,50,50,50,-67,-42,-44,-47,50,-45,]),'minus':([32,46,47,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,93,94,96,97,98,99,100,102,103,104,105,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,133,134,136,137,138,139,140,141,142,143,149,150,151,152,153,155,156,157,158,161,163,164,165,166,169,170,171,172,173,174,175,],[51,-70,87,51,51,51,51,51,51,-71,-75,-79,-80,-81,51,-82,-83,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,87,87,-49,87,-51,-72,87,-68,-69,51,-36,87,87,87,87,87,87,87,87,87,87,87,87,-60,-61,-62,-63,-64,-65,51,51,51,51,-73,-74,-34,51,87,-35,-66,51,51,87,87,87,87,-37,87,87,51,51,51,51,-67,87,87,87,87,51,87,]),'not':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,96,97,98,99,102,103,104,105,107,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,133,134,136,137,138,139,140,141,142,143,149,150,151,152,153,155,157,158,163,164,165,166,169,170,171,173,174,175,],[52,-70,52,52,52,52,52,52,-71,-75,-79,-80,-81,52,-82,-83,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,-49,-50,-51,-72,-68,-69,52,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,52,52,52,52,-73,-74,-34,52,-40,-35,-66,52,52,-41,-43,-46,-37,-39,52,52,52,52,-67,-42,-44,-47,52,-45,]),'isnull':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,96,97,98,99,102,103,104,105,107,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,133,134,136,137,138,139,140,141,142,143,149,150,151,152,153,155,157,158,163,164,165,166,169,170,171,173,174,175,],[53,-70,53,53,53,53,53,53,-71,-75,-79,-80,-81,53,-82,-83,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,-49,-50,-51,-72,-68,-69,53,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,53,53,53,53,-73,-74,-34,53,-40,-35,-66,53,53,-41,-43,-46,-37,-39,53,53,53,53,-67,-42,-44,-47,53,-45,]),'new':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,96,97,98,99,102,103,104,105,107,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,133,134,136,137,138,139,140,141,142,143,149,150,151,152,153,155,157,158,163,164,165,166,169,170,171,173,174,175,],[55,-70,55,55,55,55,55,55,-71,-75,-79,-80,-81,55,-82,-83,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,-49,-50,-51,-72,-68,-69,55,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,55,55,55,55,-73,-74,-34,55,-40,-35,-66,55,55,-41,-43,-46,-37,-39,55,55,55,55,-67,-42,-44,-47,55,-45,]),'integer_literal':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,96,97,98,99,102,103,104,105,107,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,133,134,136,137,138,139,140,141,142,143,149,150,151,152,153,155,157,158,163,164,165,166,169,170,171,173,174,175,],[58,-70,58,58,58,58,58,58,-71,-75,-79,-80,-81,58,-82,-83,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,-49,-50,-51,-72,-68,-69,58,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,58,58,58,58,-73,-74,-34,58,-40,-35,-66,58,58,-41,-43,-46,-37,-39,58,58,58,58,-67,-42,-44,-47,58,-45,]),'string_literal':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,96,97,98,99,102,103,104,105,107,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,133,134,136,137,138,139,140,141,142,143,149,150,151,152,153,155,157,158,163,164,165,166,169,170,171,173,174,175,],[59,-70,59,59,59,59,59,59,-71,-75,-79,-80,-81,59,-82,-83,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,-49,-50,-51,-72,-68,-69,59,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,59,59,59,59,-73,-74,-34,59,-40,-35,-66,59,59,-41,-43,-46,-37,-39,59,59,59,59,-67,-42,-44,-47,59,-45,]),'true':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,96,97,98,99,102,103,104,105,107,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,133,134,136,137,138,139,140,141,142,143,149,150,151,152,153,155,157,158,163,164,165,166,169,170,171,173,174,175,],[62,-70,62,62,62,62,62,62,-71,-75,-79,-80,-81,62,-82,-83,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,-49,-50,-51,-72,-68,-69,62,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,62,62,62,62,-73,-74,-34,62,-40,-35,-66,62,62,-41,-43,-46,-37,-39,62,62,62,62,-67,-42,-44,-47,62,-45,]),'false':([32,46,48,49,51,52,53,54,56,57,58,59,60,61,62,63,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,96,97,98,99,102,103,104,105,107,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,133,134,136,137,138,139,140,141,142,143,149,150,151,152,153,155,157,158,163,164,165,166,169,170,171,173,174,175,],[63,-70,63,63,63,63,63,63,-71,-75,-79,-80,-81,63,-82,-83,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,-49,-50,-51,-72,-68,-69,63,-36,-38,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,63,63,63,63,-73,-74,-34,63,-40,-35,-66,63,63,-41,-43,-46,-37,-39,63,63,63,63,-67,-42,-44,-47,63,-45,]),'rpar':([33,41,42,43,44,45,46,54,56,57,58,59,60,62,63,64,65,66,67,76,96,97,98,99,100,101,102,103,105,111,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,143,144,146,149,151,152,153,155,157,161,162,169,170,171,173,175,],[-28,-23,-24,-25,-26,-27,-70,99,-71,-75,-79,-80,-81,-82,-83,-33,109,112,-29,-76,-49,-50,-51,-72,138,139,-68,-69,-36,-31,-48,149,-77,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,-73,-74,-34,-35,-32,-30,-66,-76,-41,-43,-46,-37,-78,169,-67,-42,-44,-47,-45,]),'comma':([33,41,42,43,44,45,46,56,57,58,59,60,62,63,64,65,67,76,96,97,98,99,102,103,105,111,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,143,144,146,149,151,152,153,155,157,161,162,169,170,171,173,175,],[-28,-23,-24,-25,-26,-27,-70,-71,-75,-79,-80,-81,-82,-83,-33,110,-29,-76,-49,-50,-51,-72,-68,-69,-36,-31,-48,150,-77,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,-73,-74,-34,-35,-32,-30,-66,-76,-41,-43,-46,-37,-78,150,-67,-42,-44,-47,-45,]),'in':([41,42,43,44,45,46,56,57,58,59,60,62,63,95,96,97,98,99,102,103,105,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,143,149,152,153,154,155,156,157,169,170,171,172,173,175,],[-23,-24,-25,-26,-27,-70,-71,-75,-79,-80,-81,-82,-83,136,-49,-50,-51,-72,-68,-69,-36,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,-73,-74,-34,-35,-66,-41,-43,164,-46,166,-37,-67,-42,-44,174,-47,-45,]),'and':([46,47,56,57,58,59,60,62,63,93,94,96,97,98,99,100,102,103,105,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,142,143,149,152,153,155,156,157,158,161,169,170,171,172,173,175,],[-70,78,-71,-75,-79,-80,-81,-82,-83,78,78,-49,-50,-51,-72,78,-68,-69,-36,78,78,78,78,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,-73,-74,-34,78,-35,-66,78,78,78,78,-37,78,78,-67,78,78,78,78,78,]),'or':([46,47,56,57,58,59,60,62,63,93,94,96,97,98,99,100,102,103,105,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,142,143,149,152,153,155,156,157,158,161,169,170,171,172,173,175,],[-70,79,-71,-75,-79,-80,-81,-82,-83,79,79,-49,-50,-51,-72,79,-68,-69,-36,79,79,79,79,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,-73,-74,-34,79,-35,-66,79,79,79,79,-37,79,79,-67,79,79,79,79,79,]),'xor':([46,47,56,57,58,59,60,62,63,93,94,96,97,98,99,100,102,103,105,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,142,143,149,152,153,155,156,157,158,161,169,170,171,172,173,175,],[-70,80,-71,-75,-79,-80,-81,-82,-83,80,80,-49,-50,-51,-72,80,-68,-69,-36,80,80,80,80,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,-73,-74,-34,80,-35,-66,80,80,80,80,-37,80,80,-67,80,80,80,80,80,]),'equal':([46,47,56,57,58,59,60,62,63,93,94,96,97,98,99,100,102,103,105,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,142,143,149,152,153,155,156,157,158,161,169,170,171,172,173,175,],[-70,81,-71,-75,-79,-80,-81,-82,-83,81,81,-49,81,-51,-72,81,-68,-69,-36,81,81,81,81,81,81,81,None,None,None,None,None,-60,-61,-62,-63,-64,-65,-73,-74,-34,81,-35,-66,81,81,81,81,-37,81,81,-67,81,81,81,81,81,]),'lower':([46,47,56,57,58,59,60,62,63,93,94,96,97,98,99,100,102,103,105,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,142,143,149,152,153,155,156,157,158,161,169,170,171,172,173,175,],[-70,82,-71,-75,-79,-80,-81,-82,-83,82,82,-49,82,-51,-72,82,-68,-69,-36,82,82,82,82,82,82,82,None,None,None,None,None,-60,-61,-62,-63,-64,-65,-73,-74,-34,82,-35,-66,82,82,82,82,-37,82,82,-67,82,82,82,82,82,]),'larger':([46,47,56,57,58,59,60,62,63,93,94,96,97,98,99,100,102,103,105,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,142,143,149,152,153,155,156,157,158,161,169,170,171,172,173,175,],[-70,83,-71,-75,-79,-80,-81,-82,-83,83,83,-49,83,-51,-72,83,-68,-69,-36,83,83,83,83,83,83,83,None,None,None,None,None,-60,-61,-62,-63,-64,-65,-73,-74,-34,83,-35,-66,83,83,83,83,-37,83,83,-67,83,83,83,83,83,]),'lower_equal':([46,47,56,57,58,59,60,62,63,93,94,96,97,98,99,100,102,103,105,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,142,143,149,152,153,155,156,157,158,161,169,170,171,172,173,175,],[-70,84,-71,-75,-79,-80,-81,-82,-83,84,84,-49,84,-51,-72,84,-68,-69,-36,84,84,84,84,84,84,84,None,None,None,None,None,-60,-61,-62,-63,-64,-65,-73,-74,-34,84,-35,-66,84,84,84,84,-37,84,84,-67,84,84,84,84,84,]),'larger_equal':([46,47,56,57,58,59,60,62,63,93,94,96,97,98,99,100,102,103,105,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,142,143,149,152,153,155,156,157,158,161,169,170,171,172,173,175,],[-70,85,-71,-75,-79,-80,-81,-82,-83,85,85,-49,85,-51,-72,85,-68,-69,-36,85,85,85,85,85,85,85,None,None,None,None,None,-60,-61,-62,-63,-64,-65,-73,-74,-34,85,-35,-66,85,85,85,85,-37,85,85,-67,85,85,85,85,85,]),'plus':([46,47,56,57,58,59,60,62,63,93,94,96,97,98,99,100,102,103,105,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,142,143,149,152,153,155,156,157,158,161,169,170,171,172,173,175,],[-70,86,-71,-75,-79,-80,-81,-82,-83,86,86,-49,86,-51,-72,86,-68,-69,-36,86,86,86,86,86,86,86,86,86,86,86,86,-60,-61,-62,-63,-64,-65,-73,-74,-34,86,-35,-66,86,86,86,86,-37,86,86,-67,86,86,86,86,86,]),'times':([46,47,56,57,58,59,60,62,63,93,94,96,97,98,99,100,102,103,105,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,142,143,149,152,153,155,156,157,158,161,169,170,171,172,173,175,],[-70,88,-71,-75,-79,-80,-81,-82,-83,88,88,-49,88,-51,-72,88,-68,-69,-36,88,88,88,88,88,88,88,88,88,88,88,88,88,88,-62,-63,-64,-65,-73,-74,-34,88,-35,-66,88,88,88,88,-37,88,88,-67,88,88,88,88,88,]),'div':([46,47,56,57,58,59,60,62,63,93,94,96,97,98,99,100,102,103,105,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,142,143,149,152,153,155,156,157,158,161,169,170,171,172,173,175,],[-70,89,-71,-75,-79,-80,-81,-82,-83,89,89,-49,89,-51,-72,89,-68,-69,-36,89,89,89,89,89,89,89,89,89,89,89,89,89,89,-62,-63,-64,-65,-73,-74,-34,89,-35,-66,89,89,89,89,-37,89,89,-67,89,89,89,89,89,]),'modulo':([46,47,56,57,58,59,60,62,63,93,94,96,97,98,99,100,102,103,105,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,142,143,149,152,153,155,156,157,158,161,169,170,171,172,173,175,],[-70,90,-71,-75,-79,-80,-81,-82,-83,90,90,-49,90,-51,-72,90,-68,-69,-36,90,90,90,90,90,90,90,90,90,90,90,90,90,90,-62,-63,-64,-65,-73,-74,-34,90,-35,-66,90,90,90,90,-37,90,90,-67,90,90,90,90,90,]),'pow':([46,47,56,57,58,59,60,62,63,93,94,96,97,98,99,100,102,103,105,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,142,143,149,152,153,155,156,157,158,161,169,170,171,172,173,175,],[-70,91,-71,-75,-79,-80,-81,-82,-83,91,91,91,91,91,-72,91,-68,-69,-36,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,-73,-74,-34,91,-35,-66,91,91,91,91,-37,91,91,-67,91,91,91,91,91,]),'dot':([46,47,56,57,58,59,60,62,63,93,94,96,97,98,99,100,102,103,105,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,142,143,149,152,153,155,156,157,158,161,169,170,171,172,173,175,],[-70,92,-71,-75,-79,-80,-81,-82,-83,92,92,92,92,92,-72,92,-68,-69,-36,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,-73,-74,-34,92,-35,-66,92,92,92,92,-37,92,92,-67,92,92,92,92,92,]),'then':([46,56,57,58,59,60,62,63,93,96,97,98,99,102,103,105,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,143,149,152,153,155,157,169,170,171,173,175,],[-70,-71,-75,-79,-80,-81,-82,-83,133,-49,-50,-51,-72,-68,-69,-36,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,-73,-74,-34,-35,-66,-41,-43,-46,-37,-67,-42,-44,-47,-45,]),'do':([46,56,57,58,59,60,62,63,94,96,97,98,99,102,103,105,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,143,149,152,153,155,157,169,170,171,173,175,],[-70,-71,-75,-79,-80,-81,-82,-83,134,-49,-50,-51,-72,-68,-69,-36,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,-73,-74,-34,-35,-66,-41,-43,-46,-37,-67,-42,-44,-47,-45,]),'else':([46,56,57,58,59,60,62,63,96,97,98,99,102,103,105,115,118,119,120,121,122,123,124,125,126,127,128,129,130,131,138,139,140,143,149,152,153,155,157,169,170,171,173,175,],[-70,-71,-75,-79,-80,-81,-82,-83,-49,-50,-51,-72,-68,-69,-36,-48,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-65,-73,-74,-34,-35,-66,163,-43,-46,-37,-67,-42,-44,-47,-45,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'Program':([0,],[1,]),'Class':([0,1,],[2,4,]),'Class_body':([6,9,23,28,29,36,],[11,15,34,37,39,69,]),'Field':([11,15,34,37,39,69,],[20,20,20,20,20,20,]),'Method':([11,15,34,37,39,69,],[21,21,21,21,21,21,]),'Type':([30,108,135,145,147,],[40,144,154,159,160,]),'Expr':([32,48,49,51,52,53,54,61,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,104,133,134,136,137,141,150,151,163,164,165,166,174,],[47,93,94,96,97,98,100,107,114,115,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,142,152,153,155,156,158,161,117,170,171,172,173,175,]),'Literal':([32,48,49,51,52,53,54,61,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,104,133,134,136,137,141,150,151,163,164,165,166,174,],[56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,]),'Block':([32,48,49,51,52,53,54,61,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,104,133,134,136,137,141,150,151,159,160,163,164,165,166,174,],[57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,167,168,57,57,57,57,57,]),'Boolean_literal':([32,48,49,51,52,53,54,61,74,75,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,104,133,134,136,137,141,150,151,163,164,165,166,174,],[60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,]),'Formals':([33,],[65,]),'Formal':([33,65,110,],[67,111,146,]),'Block_body':([61,],[104,]),'Args':([76,151,],[116,162,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> Program","S'",1,None,None,None),
  ('Program -> Class','Program',1,'p_Program','myParserExt.py',48),
  ('Program -> Program Class','Program',2,'p_Program','myParserExt.py',49),
  ('Class_body -> <empty>','Class_body',0,'p_Class_body','myParserExt.py',58),
  ('Class_body -> Class_body Field','Class_body',2,'p_Class_body','myParserExt.py',59),
  ('Class_body -> Class_body Method','Class_body',2,'p_Class_body','myParserExt.py',60),
  ('Class -> class type_identifier lbrace Class_body rbrace','Class',5,'p_Class','myParserExt.py',71),
  ('Class -> class type_identifier extends type_identifier lbrace Class_body rbrace','Class',7,'p_Class','myParserExt.py',72),
  ('Class -> class type_identifier lbrace error rbrace','Class',5,'p_Class_error','myParserExt.py',88),
  ('Class -> class type_identifier extends type_identifier lbrace error rbrace','Class',7,'p_Class_error','myParserExt.py',89),
  ('Class -> class lbrace Class_body rbrace','Class',4,'p_Class_error_no_name','myParserExt.py',96),
  ('Class -> class extends type_identifier lbrace Class_body rbrace','Class',6,'p_Class_error_no_name','myParserExt.py',97),
  ('Class -> class object_identifier lbrace error rbrace','Class',5,'p_Class_error_object_id_name','myParserExt.py',106),
  ('Class -> class object_identifier extends type_identifier lbrace Class_body rbrace','Class',7,'p_Class_error_object_id_name','myParserExt.py',107),
  ('Class -> class type_identifier extends object_identifier lbrace Class_body rbrace','Class',7,'p_Class_error_object_id_name_parent','myParserExt.py',116),
  ('Field -> object_identifier colon Type semicolon','Field',4,'p_Field','myParserExt.py',124),
  ('Field -> object_identifier colon Type assign Expr semicolon','Field',6,'p_Field','myParserExt.py',125),
  ('Field -> object_identifier colon Type','Field',3,'p_Field_error_semicolon','myParserExt.py',136),
  ('Field -> object_identifier colon Type assign Expr','Field',5,'p_Field_error_semicolon','myParserExt.py',137),
  ('Field -> object_identifier semicolon','Field',2,'p_Field_error_type','myParserExt.py',151),
  ('Field -> object_identifier assign Expr semicolon','Field',4,'p_Field_error_type','myParserExt.py',152),
  ('Method -> object_identifier lpar Formals rpar colon Type Block','Method',7,'p_Method','myParserExt.py',165),
  ('Method -> object_identifier lpar error rpar colon Type Block','Method',7,'p_Method_error','myParserExt.py',171),
  ('Type -> type_identifier','Type',1,'p_Type','myParserExt.py',179),
  ('Type -> int32','Type',1,'p_Type','myParserExt.py',180),
  ('Type -> bool','Type',1,'p_Type','myParserExt.py',181),
  ('Type -> string','Type',1,'p_Type','myParserExt.py',182),
  ('Type -> unit','Type',1,'p_Type','myParserExt.py',183),
  ('Formals -> <empty>','Formals',0,'p_Formals','myParserExt.py',188),
  ('Formals -> Formal','Formals',1,'p_Formals','myParserExt.py',189),
  ('Formals -> Formals comma Formal','Formals',3,'p_Formals','myParserExt.py',190),
  ('Formals -> Formals Formal','Formals',2,'p_Formals_error_comma','myParserExt.py',205),
  ('Formal -> object_identifier colon Type','Formal',3,'p_Formal','myParserExt.py',213),
  ('Formal -> object_identifier','Formal',1,'p_Formals_error_type','myParserExt.py',219),
  ('Block -> lbrace Block_body rbrace','Block',3,'p_Block','myParserExt.py',227),
  ('Block -> lbrace error rbrace','Block',3,'p_Block_error','myParserExt.py',232),
  ('Block -> lbrace rbrace','Block',2,'p_Block_error_empty','myParserExt.py',241),
  ('Block -> lbrace Block_body semicolon rbrace','Block',4,'p_Block_error_end_semicolon','myParserExt.py',250),
  ('Block_body -> Expr','Block_body',1,'p_Block_body','myParserExt.py',257),
  ('Block_body -> Block_body semicolon Expr','Block_body',3,'p_Block_body','myParserExt.py',258),
  ('Block_body -> Block_body Expr','Block_body',2,'p_Block_body_error_expr_semicolon','myParserExt.py',270),
  ('Expr -> if Expr then Expr','Expr',4,'p_Expr_If_then','myParserExt.py',278),
  ('Expr -> if Expr then Expr else Expr','Expr',6,'p_Expr_If_then','myParserExt.py',279),
  ('Expr -> while Expr do Expr','Expr',4,'p_Expr_while','myParserExt.py',289),
  ('Expr -> let object_identifier colon Type in Expr','Expr',6,'p_Expr_let','myParserExt.py',294),
  ('Expr -> let object_identifier colon Type assign Expr in Expr','Expr',8,'p_Expr_let','myParserExt.py',295),
  ('Expr -> let object_identifier in Expr','Expr',4,'p_Expr_let_error_type','myParserExt.py',306),
  ('Expr -> let object_identifier assign Expr in Expr','Expr',6,'p_Expr_let_error_type','myParserExt.py',307),
  ('Expr -> object_identifier assign Expr','Expr',3,'p_Expr_assign','myParserExt.py',320),
  ('Expr -> minus Expr','Expr',2,'p_Expr_uminus','myParserExt.py',325),
  ('Expr -> not Expr','Expr',2,'p_Expr_UnOp','myParserExt.py',330),
  ('Expr -> isnull Expr','Expr',2,'p_Expr_UnOp','myParserExt.py',331),
  ('Expr -> Expr and Expr','Expr',3,'p_Expr_BinOp','myParserExt.py',336),
  ('Expr -> Expr or Expr','Expr',3,'p_Expr_BinOp','myParserExt.py',337),
  ('Expr -> Expr xor Expr','Expr',3,'p_Expr_BinOp','myParserExt.py',338),
  ('Expr -> Expr equal Expr','Expr',3,'p_Expr_BinOp','myParserExt.py',339),
  ('Expr -> Expr lower Expr','Expr',3,'p_Expr_BinOp','myParserExt.py',340),
  ('Expr -> Expr larger Expr','Expr',3,'p_Expr_BinOp','myParserExt.py',341),
  ('Expr -> Expr lower_equal Expr','Expr',3,'p_Expr_BinOp','myParserExt.py',342),
  ('Expr -> Expr larger_equal Expr','Expr',3,'p_Expr_BinOp','myParserExt.py',343),
  ('Expr -> Expr plus Expr','Expr',3,'p_Expr_BinOp','myParserExt.py',344),
  ('Expr -> Expr minus Expr','Expr',3,'p_Expr_BinOp','myParserExt.py',345),
  ('Expr -> Expr times Expr','Expr',3,'p_Expr_BinOp','myParserExt.py',346),
  ('Expr -> Expr div Expr','Expr',3,'p_Expr_BinOp','myParserExt.py',347),
  ('Expr -> Expr modulo Expr','Expr',3,'p_Expr_BinOp','myParserExt.py',348),
  ('Expr -> Expr pow Expr','Expr',3,'p_Expr_BinOp','myParserExt.py',349),
  ('Expr -> object_identifier lpar Args rpar','Expr',4,'p_Expr_Call','myParserExt.py',355),
  ('Expr -> Expr dot object_identifier lpar Args rpar','Expr',6,'p_Expr_Call','myParserExt.py',356),
  ('Expr -> new type_identifier','Expr',2,'p_Expr_New','myParserExt.py',367),
  ('Expr -> new object_identifier','Expr',2,'p_Expr_New_error_obj_id','myParserExt.py',373),
  ('Expr -> object_identifier','Expr',1,'p_Expr_Object_id','myParserExt.py',381),
  ('Expr -> Literal','Expr',1,'p_Expr_literal','myParserExt.py',386),
  ('Expr -> lpar rpar','Expr',2,'p_Expr_Unit','myParserExt.py',391),
  ('Expr -> lpar Expr rpar','Expr',3,'p_Expr_Par_expr','myParserExt.py',396),
  ('Expr -> lpar error rpar','Expr',3,'p_Expr_Par_expr_error','myParserExt.py',402),
  ('Expr -> Block','Expr',1,'p_Expr_block','myParserExt.py',410),
  ('Args -> <empty>','Args',0,'p_Args','myParserExt.py',415),
  ('Args -> Expr','Args',1,'p_Args','myParserExt.py',416),
  ('Args -> Args comma Expr','Args',3,'p_Args','myParserExt.py',417),
  ('Literal -> integer_literal','Literal',1,'p_Literal','myParserExt.py',430),
  ('Literal -> string_literal','Literal',1,'p_Literal','myParserExt.py',431),
  ('Literal -> Boolean_literal','Literal',1,'p_Literal','myParserExt.py',432),
  ('Boolean_literal -> true','Boolean_literal',1,'p_Boolean_literal','myParserExt.py',440),
  ('Boolean_literal -> false','Boolean_literal',1,'p_Boolean_literal','myParserExt.py',441),
]
