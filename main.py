import json
import os

from kivy.core.window import Window
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

import desktop_file_dialogs
from font import get_dict_gname_guni, dowloadGlyph, get_font_name, get_font_description
from kivymd.app import MDApp
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDTextButton
from kivymd.uix.label import MDIcon

# 'youtube-studio': '0xf0847',
# 'youtube':		'0xf167',
# print(pywinauto.findwindows.find_window())
# MDApp.
# kivy.graphics.Line.da
# Clock.max_iteration = 50

SAVE_FILE = "save.json"


class DropZone(AnchorLayout):
	offset = NumericProperty(10)
	color = ListProperty()

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.color = MDApp.get_running_app().theme_cls.primary_color


class icon(GridLayout):
	uicon = StringProperty()
	gfontFile = StringProperty()

	iconName = StringProperty()
	iconId = NumericProperty()
	mcolor = ListProperty()


class bicon(Button, HoverBehavior):
	uicon = StringProperty()
	gfontFile = StringProperty()

	iconName = StringProperty()
	iconId = NumericProperty()
	mcolor = ListProperty()

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.bind(texture_size=self._update_font_size)

	def _update_font_size(self, *args):
		if args[1] > self.size:
			print("trop gran: ",self.iconName)
			self.font_size -= 1
		# if args[1] < self.size:
		# 	print("trop peti: ",self.iconName)
		# 	self.font_size += 1
			# data = []
			# change=False
			# pprint(dir(self.parent.parent))
			# for e in self.parent.parent.data:
			# 	if e["iconName"] == self.iconName:
			# 		if "font_size" in e.keys():
			# 			print(self.iconName)
			# 			e["font_size"] -= 1
			# 		else:
			# 			e["font_size"] = 40
			# 	data.append(e)
			# self.parent.parent.data=data
			#
			# self.parent.parent.refresh_views()
		# tolerance = 0
		# if self.texture_size[0] > self.width or self.texture_size[1] > self.height:
		# 	self.font_size -= 1
		# elif max(self.texture_size[0] - self.width, self.texture_size[1] - self.height) > tolerance:
		# 	self.font_size += 1

	def _on_press(self, widg):
		# self.parent.parent.refresh_from_data()
		# if not self.wlo == "":
		app = MDApp.get_running_app()
		#	 if app.islock:
		#		 print("devenu blan")
		#		 self.edit_bg(app.wlo, [0, 0, 0, 0])
		#	 else:
		#		 app.wlo = widg
		#		 self.edit_bg(app.wlo,[0, 0, 0, 0.3])
		app.lock()

	#
	#	 # pprint(self.parent.parent.data)
	# def edit_bg(self,wid,color):
	#	 for index, element in enumerate(wid.parent.parent.data):
	#		 if element["iconName"] == wid.iconName:
	#			 element["background_color"] = color
	#			 self.parent.parent.data[index] = element
	#	 self.parent.parent.refresh_from_data()
	def _on_leave(self, widg):
		app = MDApp.get_running_app()
		self.background_color = [0, 0, 0, 0] if not self == app.wlo else self.background_color

	def _on_enter(self, widg):
		app = MDApp.get_running_app()
		self.background_color = [0, 0, 0, 0.1] if not self == app.wlo else self.background_color
		app.set_preview(self.iconName, False)


class jicon(MDIcon):
	uicon = StringProperty()
	gfontFile = StringProperty()


class FontExplorer(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Window.bind(on_resize=self.on_resize)
		Window.bind(on_maximize=self.on_resize)

	# Window.bind(on_scroll=self.check_size)
	def chexk_size(self):
		for x in self.ids.rgl.children:
			if x.width > 100:
				print(x.font_size)
				x.font_size = 10
			else:
				x.font_size = 40
	def download(self):
		dowloadGlyph(
			size=int(self.ids.downloadsize.text),
			text=self.ids.previewIcon.text,
			font=self.ids.previewIcon.font_name,
			name=self.ids.iconName.text
		)
	def search(self, word):
		# print(args)
		# return
		result = [x for x in self.glyphs if word in x]

		result.sort(key=len)
		self.ids.rv.data = []
		for glyph in result:
			if not glyph == "font-awesome-logo-ful":
				self.ids.rv.data.append(
					{
						"viewclass": "bicon",
						"text": chr(self.glyphs[glyph]),
						"font_name": self.file,
						"size_hint": (None, None),
						"iconName": glyph,
						# "size": "self.texture_size"
					})
			else:
				print(f"the glyph {glyph} has ben hidden because it was to big")

	def explore_font(self, file):
		self.file = file
		if not os.path.exists(SAVE_FILE):
			history = []
		else:
			with open(SAVE_FILE, "r") as save_file:
				history = json.load(save_file)
		if file not in history:
			history.append(file)
		else:
			history.remove(file)
			history.append(file)
		if len(history) > 5:
			history.remove(history[0])
		# pprint(history)
		with open(SAVE_FILE, "w") as save_file:
			history = json.dump(history, save_file, indent=4)
		MDApp.get_running_app().on_start()
		# self.ids.unicode.font_name = file
		self.ids.chra.font_name = file
		self.ids.previewIcon.font_name = file
		self.ids.testzone.font_name = file
		self.ids.sfontname.text = get_font_name(file)
		self.ids.sfontname.tooltip_text = get_font_description(file)
		# self.ids.iconName.font_name = file
		self.glyphs = get_dict_gname_guni(file)
		MDApp.get_running_app().glyphs = self.glyphs
		self.ids.rv.data = []
		for glyph in self.glyphs.keys():
			if not glyph == "font-awesome-logo-ful":
				self.ids.rv.data.append(
					{
						"viewclass": "bicon",
						"text": chr(self.glyphs[glyph]),
						"font_name": file,
						"size_hint": (None, None),
						"iconName": glyph,
						# "size": "self.texture_size"
					}
				)

			else:
				print(f"the glyph {glyph} has ben hidden because it was to big")
		self.on_resize()

	# {
	#		"viewclass": "icon",
	#		"uicon": chr(glyphs[glyph]),
	#		"gfontFile": file,
	#		 "size_hint": (None, None)
	#		# "iconName": glyph,
	#		# "size": "self.texture_size"
	#	 }
	# {
	#	"viewclass": "MDIcon",
	#	"text": chr(glyphs[glyph]),
	#	"font_name": file,
	#	"halign": "center",
	#	"size_hint": (None,None)
	# }

	# self.ids.rv.data.append(
	#		 {
	#			 "viewclass": "icon",
	#			 "uicon": chr(glyphs[glyph]),
	#			 "gfontFile": file,
	#			 "iconName":glyph,
	#			 "iconId":random.randrange(1,100),
	#			 "mcolor": (0, 1, 0, 0.2)
	#		 }
	#	 )

	def on_resize(self, *args):
		try:
			# print(self.file)

			RecycleGridLayout = self.ids.rgl
			RecycleGridLayout.cols = int(
				(RecycleGridLayout.width // RecycleGridLayout.children[0].width) if len(self.children) > 0 else 0)

		# print(int((RecycleGridLayout.width // RecycleGridLayout.children[0].width) if len(self.children) > 0 else 0))
		# if args[1] > 1300:
		#	 print("-2")
		#	 RecycleGridLayout.cols = int(
		#		 (RecycleGridLayout.width // RecycleGridLayout.children[0].width) - 3 if len(self.children) > 0 else 0)
		# elif args[1] > 1000:
		#	 print("-1")
		#	 RecycleGridLayout.cols = int(
		#		 (RecycleGridLayout.width // RecycleGridLayout.children[0].width) - 2 if len(self.children) > 0 else 0)
		# elif args[1] > 500:
		#	 print("-1")
		#	 RecycleGridLayout.cols = int(
		#		 (RecycleGridLayout.width // RecycleGridLayout.children[0].width) - 1 if len(self.children) > 0 else 0)
		# else:
		#	 print("-0")
		#	 RecycleGridLayout.cols = int(
		#		 (RecycleGridLayout.width // RecycleGridLayout.children[0].width) if len(
		#			 self.children) > 0 else 0)
		except Exception as e:
			print("erreur dans on resize: " + str(e))

	# self.ids.rv_fav.data.append(
	#	 {
	#		 "viewclass": "TwoLineStarIconListItem",
	#		 "icon": name_icon,
	#		 "text": name_icon,
	#		 "secondary_text": str(code_icon),
	#		 "favorite": False
	#	 }
	# )


class CustomDropDown(DropDown):
	pass


class historty_label(MDTextButton):
	pass


# BoxLayout.si
class mainApp(MDApp):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Window.bind(on_dropfile=self._on_file_drop)
		self.islock = False
		self.wlo = Widget()
		self.line_color = [0.7, 0.7, 0.7, 1]

	def on_start(self):
		# AnchorLayout().add_widget()
		for torem in self.root.ids.dropzone.ids.historybox.children:
			self.root.ids.dropzone.ids.historybox.remove_widget(torem)
		for torem in self.root.ids.dropzone.ids.historybox.children:
			self.root.ids.dropzone.ids.historybox.remove_widget(torem)
		for torem in self.root.ids.dropzone.ids.historybox.children:
			self.root.ids.dropzone.ids.historybox.remove_widget(torem)

		if os.path.exists(SAVE_FILE):
			with open(SAVE_FILE, "r") as save_file:
				history = json.load(save_file)
				history.reverse()
			for font in history:
				self.root.ids.dropzone.ids.historybox.add_widget(
					historty_label(
						text=font,

					)
				)
			self.root.ids.dropzone.ids.historybox.add_widget(Widget())

	# pprint(dir(Window))

	def _on_file_drop(self, window, file_path):

		Window.raise_window()
		self.openfont(file_path.decode("utf-8"))

	# self.width // self.children[0].width if len(self.children) > 0 else
	# str.encode()
	def lock(self):
		# print("avant", self.islock)
		self.islock = not self.islock

	# print("appres", self.islock)
	def set_preview(self, name, persistent):
		# pass
		# self.root.ids.unicode.text = self.glyphs[name]
		# print("lock",self.islock)
		if not self.islock:
			self.root.ids.fontexplorer.ids.unicode.text = str(hex(self.glyphs[name]))[2:]
			self.root.ids.fontexplorer.ids.unicodeid.text = str(self.glyphs[name])
			self.root.ids.fontexplorer.ids.chra.text = chr(self.glyphs[name])
			self.root.ids.fontexplorer.ids.previewIcon.text = str(chr(self.glyphs[name]))
			self.root.ids.fontexplorer.ids.iconName.text = str(name)

	def manualSelect(self):
		self.curentFont = (desktop_file_dialogs.Desktop_FileDialog(
			title="Select File",
			initial_directory=".",
			file_groups=[
				desktop_file_dialogs.FileGroup(name="Font files", extensions=["ttf"]),
				desktop_file_dialogs.FileGroup.All_FileTypes,
			],
		).show())
		Window.raise_window()
		if self.curentFont:
			# print(self.root.ids)
			self.openfont(self.curentFont)
			self.root.ids.fontexplorer.explore_font(self.curentFont)
			self.root.ids.scrennm.current = "fontexplorer"

		# self.root.add_widget(FontExplorer(id="fontexplorer"))
		# print(self.root.ids)

	def openfont(self, file):
		self.root.ids.fontexplorer.explore_font(file)
		self.root.ids.scrennm.current = "fontexplorer"

	def openNewFont(self, *args):
		# print(self.root.ids)
		self.root.ids.scrennm.current = "dropzone"
	# self.root.remove_widget(self.root.ids.dropzone)
	# self.root.add_widget(DropZone(id="dropzone", offset=25))

mainApp().run()



