import eyed3
import glob
import wx
import numpy as np
from imagefilters import ImageFilters

class EditDialog(wx.Dialog):
    def __init__(self, mp3):
        title = f'Editing "{mp3.tag.title}"'
        super().__init__(parent = None, title = title)
        self.mp3 = mp3
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.artist = wx.TextCtrl(self, value = self.mp3.tag.artist)
        self.add_widgets('Artist', self.artist)
        self.album = wx.TextCtrl(self, value = self.mp3.tag.album)
        self.add_widgets('Album', self.album)
        self.title = wx.TextCtrl(self, value = self.mp3.tag.title)
        self.add_widgets('Title',self.title)
        btn_sizer = wx.BoxSizer()
        save_btn = wx.Button(self, label = 'Save')
        save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        btn_sizer.Add(save_btn, 0, wx.ALL, 5)
        btn_sizer.Add(wx.Button(self, id = wx.ID_CANCEL), 0, wx.ALL, 5)
        self.main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizer(self.main_sizer)

    def add_widgets(self, label_text, text_ctrl):
        row_sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, label=label_text, size = (50, -1))
        row_sizer.Add(label, 0, wx.ALL, 5)
        row_sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Add(row_sizer, 0, wx.EXPAND)

    def on_save(self, event):
        self.mp3.tag.artist = self.artist.GetValue()
        self.mp3.tag.album = self.album.GetValue()
        self.mp3.tag.title = self.title.GetValue()
        self.mp3.tag.save()
        self.Close()

class ImageEditorPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = parent
        self.init_panel_ui()
        '''main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.row_obj_dict = {}

        self.list_ctrl = wx.ListCtrl(self, size = (-1,100),
                                     style = wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, 'Artist', width = 140)
        self.list_ctrl.InsertColumn(1, 'Album', width = 140)
        self.list_ctrl.InsertColumn(2, 'Title', width = 200)
        main_sizer.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        edit_button = wx.Button(self, label = 'Edit')
        edit_button.Bind(wx.EVT_BUTTON, self.on_edit)
        main_sizer.Add(edit_button, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(main_sizer)'''

    def init_panel_ui(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        #self.st_ip_image = wx.StaticText(self, label = 'Input Image')
        #main_sizer.Add(self.st_ip_image, 0, wx.ALL | wx.EXPAND, 5)
        self.bt_ip_image = wx.Button(self, label = 'Select Input Image')
        self.bt_ip_image.Bind(wx.EVT_BUTTON, self.on_select_image)
        self.main_sizer.Add(self.bt_ip_image, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.st_ip_image_path = wx.StaticText(self, label = 'Input Image path')
        hbox.Add(self.st_ip_image_path, 0, wx.ALL | wx.ALIGN_LEFT | wx.EXPAND, 5)

        self.tc_ip_image_path = wx.TextCtrl(self, id=wx.ID_ANY, value='example for text ctrl contents',
                                            pos=wx.DefaultPosition, style=wx.TE_READONLY)

        self.bt_apply_filter = wx.Button(self, label = 'Apply image filter')
        self.bt_apply_filter.Bind(wx.EVT_BUTTON, self.on_apply_filter)
        self.main_sizer.Add(self.bt_apply_filter, 0, wx.ALL | wx.ALIGN_LEFT, 5)

        self.tc_ip_image_path.SetMinSize((300, 19))
        hbox.Add(self.tc_ip_image_path, 0, wx.ALL, 5)

        #self.SetSizer(hbox)
        self.main_sizer.Add(hbox, 0, wx.ALL| wx.ALIGN_LEFT | wx.EXPAND, 5)

        self.image_filters = ['Mono', 'GammaControl', 'DocumentScanner']
        self.cb = wx.ComboBox(self, choices = self.image_filters, value = self.image_filters[0])
        self.main_sizer.Add(self.cb, 0, wx.ALL | wx.ALIGN_LEFT, 5)

        self.img = wx.Image(320, 240)
        self.static_bitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.img))
        self.img2 = wx.Image(320, 240)
        self.static_bitmap2 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.img2))
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.static_bitmap, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.static_bitmap2, 0, wx.LEFT | wx.BOTTOM | wx.RIGHT | wx.ALIGN_LEFT, 5)
        self.bt_save_img = wx.Button(self, label='Save Image')
        self.bt_save_img.Bind(wx.EVT_BUTTON, self.on_save_img)
        vbox2.Add(self.bt_save_img, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        hbox2.Add(vbox2, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.main_sizer.Add(hbox2, 0, wx.ALL | wx.ALIGN_LEFT, 5)

        self.SetSizer(self.main_sizer)
        self.main_sizer.Layout()
        self.Layout()
        self.Fit()

        #self.main_sizer.Fit(self)

    def on_apply_filter(self, event):
        print('inside on apply filter')
        filter = ImageFilters()
        gray = filter.mono()
        (h, w) = gray.shape
        color = np.stack((gray,gray,gray), axis=-1)
        print('shape of color is (%s, %s, %s)'%(color.shape))
        print(gray.dtype)
        #self.img2.Rescale(240, 180)
        #self.img2.Size((180,240))
        buf = color.tobytes()
        print(len(buf))

        self.img2 = wx.Image(w,h)
        self.img2.SetData(buf)
        self.static_bitmap2.SetBitmap(wx.Bitmap(self.img2))

        self.SetSizer(self.main_sizer)
        self.main_sizer.Layout()
        self.Fit()
        #self.frame.Fit()


        #self.img2.SetData(buf)


    def on_select_image(self, event):
        print('inside on_select_image')
        title = "Select an image"
        dlg = wx.FileDialog(self, title, style = wx.FD_OPEN)
        print(dlg.GetPath())
        #dlg = wx.DirDialog(self, title, style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.tc_ip_image_path.SetValue(dlg.GetPath())
            self.img = wx.Image(self.tc_ip_image_path.GetValue(), wx.BITMAP_TYPE_ANY)
            w = self.img.GetWidth()
            h = self.img.GetHeight()
            if w > h:
                r = 1.0 * w / h
                newW = 320
                newH = int(newW / r)
            else:
                r = 1.0 * w / h
                newH = 240
                newW = int(newH * r)
            self.img = self.img.Scale(newW, newH, quality = wx.IMAGE_QUALITY_NORMAL)
            self.static_bitmap.SetBitmap(wx.Bitmap(self.img))
            self.SetSizer(self.main_sizer)
            self.tc_ip_image_path.DoGetBestSize()
            self.Refresh()

        dlg.Destroy()


    def on_edit(self, event):
        print('in on edit')
        '''selection = self.list_ctrl.GetFocusedItem()
        if selection >=0:
            mp3 = self.row_obj_dict[selection]
            dlg = EditDialog(mp3)
            dlg.ShowModal()
            self.update_mp3_listing(self.current_folder_path)
            dlg.Destroy()'''

    def on_save_img(self, event):
        print("Save image entered")


    def update_mp3_listing(self, folder_path):
        print(folder_path)
        self.current_folder_path = folder_path
        self.list_ctrl.ClearAll()

        self.list_ctrl.InsertColumn(0, 'Artist', width=140)
        self.list_ctrl.InsertColumn(1, 'Album', width=140)
        self.list_ctrl.InsertColumn(2, 'Title', width=200)
        #self.list_ctrl.InsertColumn(3, 'Year', width=200)

        mp3s = glob.glob(folder_path + '/*.mp3')
        mp3_objects = []
        index = 0
        for mp3 in mp3s:
            mp3_object = eyed3.load(mp3)
            self.list_ctrl.InsertItem(index, mp3_object.tag.artist)
            self.list_ctrl.SetItem(index, 1, mp3_object.tag.album)
            self.list_ctrl.SetItem(index, 2, mp3_object.tag.title)
            mp3_objects.append(mp3_object)
            self.row_obj_dict[index] = mp3_object
            index += 1

class ImageEditorFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent = None, title = 'Image Editor App')
        self.panel = ImageEditorPanel(self)
        #self.create_menu()
        self.Show()
        self.Fit()

    def create_menu(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        open_folder_menu_item = file_menu.Append(wx.ID_ANY, 'Open Folder',
                                                 'Open a folder with images')
        menu_bar.Append(file_menu, '&File')
        self.Bind(event = wx.EVT_MENU, handler = self.on_open_folder,
                  source = open_folder_menu_item)
        self.SetMenuBar(menu_bar)

    def on_open_folder(self, event):
        title = "Choose a directory"
        dlg = wx.DirDialog(self, title, style = wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.panel.update_mp3_listing(dlg.GetPath())
        dlg.Destroy()

if __name__ == '__main__':
    app = wx.App(False)
    frame = ImageEditorFrame()
    app.MainLoop()