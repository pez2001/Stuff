def tokenize_parentheses(parentheses,output_file):
	parentheses = parentheses.strip(" ()")
	#parentheses = parentheses

	output_file.write("(")
	tokens = parentheses.lower().split()
	for t in tokens:
		is_name = True
		if(t == "="):
			output_file.write("==")
			is_name = False
		if(t == "true"):
			output_file.write("true")
			is_name = False
		if(t == "false"):
			output_file.write("false")
			is_name = False
		if(is_name == True):
			output_file.write(t)
	
	output_file.write(")")
	
def tokenize(input,output_file,level):
	tokens = input.lower().split()
	in_parentheses = False
	in_quotes = False
	parentheses = ""
	for t in tokens:
		is_name = True
		if(t.startswith("(")):
			in_parentheses = True
		if(t.endswith(")")):
			in_parentheses = False
			parentheses += " "
			parentheses += t				
			tokenize_parentheses(parentheses,output_file)
			continue
		if(in_parentheses):
			parentheses += " "
			parentheses += t				

		if(in_parentheses):
			continue

		if(t == "if"):
			for i in range(level):
				output_file.write("\t")
			output_file.write("if")
			is_name = False
		if(t == ":="):
			for i in range(level):
				output_file.write("\t")
			output_file.write(" = ")
			is_name = False
		if(t == "then"):
			in_if_block = True			
			for i in range(level):
				output_file.write("\t")
			output_file.write("{\n")
			level += 1
			is_name = False
		if(t == "else"):
			for i in range(level - 1):
				output_file.write("\t")
			if(in_if_block):
				output_file.write("}\n")
			output_file.write("else\n{\n")
			is_name = False
		if(t == "end_if;"):
			in_if_block = False			
			level -= 1
			for i in range(level):
				output_file.write("\t")
			output_file.write("}\n")
			is_name = False
		if(is_name == True):
			#print("name: ",t)
			for i in range(level):
				output_file.write("\t")
			output_file.write(t)
		if(t.endswith(";")):
			output_file.write("\n")
		
input = open("test.scl")
#input = open("test2.scl")
output = open("output.c","w+")
input_text = input.read()
in_if_block = False
tokenize(input_text,output,0)
print("output:\n")
print(output.read())

output.close()	