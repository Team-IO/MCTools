# MCTools
Tools for Minecraft &amp; Modding

## assemble_recipe

	assemble_recipe.py [-i input_file]... [-l lang_file]... [-o output_file] [-d] [-h]
	
	-h, --help
		Prints this help text.
	-d, --debug
		Enables further debug messages.
	-i
		Reads an input file in the json format. An example of the file structure can be seen in recipe.json.example, which contains two recipes.
		This option is allowed multiple times. If no -i is present, the default filename 'recipe.json' will be used.
	-l
		Reads a language file (simplified java properties format, item.xyz.name=XYZ Item).
		Keys are expected in the following formats.
		For namespace 'minecraft':
			item.*.name
			tile.*.name
		For other namespaces:
			item.(namespace).*.name
			tile.(namespace).*.name
		This option is allowed multiple times. If a key is not found in any of the loaded files, the key will be used as display name.
	-o
		Defines the output file to be written to.
		If no output file is specified, the default filename 'recipe.html' will be used.
