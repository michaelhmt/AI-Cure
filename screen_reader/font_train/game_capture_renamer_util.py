import os
img_dir = "this dir"
name_constant = "h_cure_font_train_game_capture"

# run this inside the game_captures_folder.
def rename_captures():
	for index, image_file in enumerate(os.listdir(img_dir)):
		num = str(index + 1).zfill(3)
		file_name = f"{name_constant}_{num}"
		new_img_name = f"{file_name}.png"
		txt_name = f"{file_name}.txt"
		os.rename(os.path.join(img_dir, image_file),
				  os.path.join(img_dir, new_img_name))

		txt_file = os.path.join(img_dir, txt_name)
		if not os.path.exists(txt_file):
			with open(os.path.join(img_dir, txt_name), "w+"):
				# just make the txt do nothing else
				pass
