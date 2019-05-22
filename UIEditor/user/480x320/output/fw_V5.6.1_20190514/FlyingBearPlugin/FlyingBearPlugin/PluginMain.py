                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ad_sent_size = 0
        self.upload_http_request = None
        self.is_uploading = False

        self.delay_auto_connect_timer = None

        self.ui_items_name = {"lb_ip","txt_printer_ip","btn_connect","btn_disconnect","lb_printer_name","lb_printer_state"
        ,"lb_printer_t0","lb_printer_t1","lb_printer_bed","btn_preheat","btn_cooldown","btn_sd","lb_gcode","txt_gcode"
        ,"btn_send","pgb_printing_progress", "lb_printing_progress","btn_pause","btn_resume","btn_stop","btn_off","lb_printing_filename","lb_printing"
        ,"btn_upload","lv_ip_list","img_edit_printer_name"}

        self.ui_items_on_normal_only = {"btn_preheat", "btn_cooldown", "btn_sd", "lb_gcode", "txt_gcode", "btn_send", "btn_upload"
        }

        self.ui_items_on_printing_only = {"pgb_printing_progress", "lb_printing_progress", "btn_pause", "btn_resume", "btn_stop", "btn_off"
        ,"lb_printing_filename", "lb_printing"
        }

        self.dialog_uploading_ui_items_name  = {"pgb_progress", "lb_remain_time", "btn_cancel", "lb_uploading_filename", "ck_auto_start_print"
        ,"lb_speed", "btn_upload"
        }

        self.dialog_file_explorer_ui_items_name = {"listview_file_explorer"}

        self.btns_name = {"btn_preheat", "btn_cooldown", "btn_sd", "btn_send", "btn_upload", "txt_gcode"}

        self.load_user_data()
        self.delay_auto_connect()

    @pyqtSlot()
    def edit_name(self):
        if self.print_id != 0:
            name, okPressed = QInputDialog.getText(None, "Edit","Printer Name", QLineEdit.Normal, self.lb_printer_name.property("text"))
            if okPressed:
                if name == "":
                    self.lb_printer_name.setProperty("text","Printer%d"%(self.print_id))
                    del(self.name_dict[str(self.print_id)])
                    self.save_user_data()
                else:
                    self.lb_printer_name.setProperty("text",name)
                    self.name_dict[str(self.print_id)] = name
                    self.save_user_data()

    @pyqtSlot(str) 
    def on_ip_list_click(self,name):
        logi("click %s"%(name))
        if len(name)>0 and self.is_ip(name):
            if self.printer_ip != name:
                self.disconnect_printer()
                self.txt_printer_ip.setProperty("text",name)
                self.connect_printer()

    def update_history_ip(self):
        data_len = len(self.ip_list)
        model = self.lv_ip_list.property("model")
        for i in range(0,model.rowCount()):
            if i<data_len:
                model.setItemData(model.createIndex(i,0), {0:self.ip_list[i]})
            else:
                model.setItemData(model.createIndex(i,0), {0:""})

    def delay_auto_connect(self):
        self.delay_auto_connect_timer = QTimer()
        self.delay_auto_connect_timer.timeout.connect(self.connect_printer)
        self.delay_auto_connect_timer.start(100)

    def save_user_data(self):
        file_path = os.path.join(os.path.expanduser('~'), "user.cfg")
        with open(file_path, 'w') as f:
            json.dump({"last_ip":self.last_ip, "last_upload_dir":self.last_upload_dir, "ip_list":self.ip_list, "name_dict":self.name_dict}, f)

    def load_user_data(self):
        file_path = os.path.join(os.path.expanduser('~'), "user.cfg")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                cfg = json.load(f)
                self.last_ip = cfg.get("last_ip")
                self.last_upload_dir = cfg.get("last_upload_dir")
                self.ip_list = cfg.get("ip_list")
                if self.ip_list is None:
                    self.ip_list = []
                self.name_dict = cfg.get("name_dict")
                if self.name_dict is None:
                    self.name_dict = {}
        
    @pyqtSlot()
    def on_window_close(self):
        self.stop_rolling_state()

    @pyqtSlot()
    def on_uploading_window_close(self):
        if self.upload_http_request:
            self.cancel_upload()

    def showPluginMainWindow(self,file_path = None):
        self.upload_file_name = file_path
        if not self.plugin_main_window:
            self.plugin_main_window = self._createDialogue('PluginMain.qml')
        self.plugin_main_window.show()
        self.bind_ui()
        self.update_status()

    def init_stage(self,root_ui_item,upload_file_name):
        self.plugin_main_window = root_ui_item
        self.upload_file_name = upload_file_name
        self.bind_ui()
        self.update_status()

    def showDialogUploading(self,file_path):
        if not self.dialog_uploading:
            self.dialog_uploading = self._createDialogue('Uploading.qml')
            for name in self.dialog_uploading_ui_items_name:
                self.dialog_uploading_ui[name] = self.dialog_uploading.findChild(QObject, name)
        self.dialog_uploading.show()
        file_name = os.path.basename(file_path)
        arr = os.path.splitext(file_name)
        name = arr[0]
        ext = arr[1] #包含.号，例 .gco
        if len(file_name) > self.MAX_FILE_NAME:
            name = name[0:self.MAX_FILE_NAME - len(ext)]
        self.start_upload("SD:/%s%s"%(name,ext),file_path)

    @pyqtSlot()
    def cancel_upload(self):
        self.dialog_uploading.hide()
        self.upload_http_request.abort()

    def _createDialogue(self,qml_filename):
        qml_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res", qml_filename)
        return Application.getInstance().createQmlComponent(qml_file_path, {"manager": self})

    def bind_ui(self):
        for name in self.ui_items_name:
            self.__dict__[name] = self.plugin_main_window.findChild(QObject, name)

        if self.printer_ip:
            self.btn_connect.setProperty('visible', False)
            self.btn_disconnect.setProperty('visible', True)
            self.txt_printer_ip.setProperty('enabled', False)
        else:
            self.btn_connect.setProperty('visible', True)
            self.btn_disconnect.setProperty('visible', False)
            self.txt_printer_ip.setProperty('enabled', True)
            if self.last_ip:
                   self.txt_printer_ip.setProperty('text', self.last_ip) 
        self.update_history_ip()

    def update_status(self):
        name = "Printer%d"%(self.print_id)
        if str(self.print_id) in self.name_dict:
            name = self.name_dict.get(str(self.print_id))

        self.lb_printer_name.setProperty('text', name)
        self.lb_printer_state.setProperty('text', self.state_dic[self.connect_state])

        self.lb_printer_t0.setProperty('text', "Extruder1 %d/%d"%(self.temp_nozzle0, self.temp_nozzle_target0 if self.is_nozzle_heating0 else 0))

        if self.nozzle_count > 1:
            self.lb_printer_t1.setProperty('visible',True)
            self.lb_printer_t1.setProperty('text', "Extruder2 %d/%d"%(self.temp_nozzle1, self.temp_nozzle_target1 if self.is_nozzle_heating1 else 0))
        else:
            self.lb_printer_t1.setProperty('visible',False)

        self.lb_printer_bed.setProperty('text', "Bed %d/%d"%(self.temp_bed, self.temp_bed_target if self.is_bed_heating else 0))

        if self.is_printing:
            for name in self.ui_items_on_printing_only:
                self.__dict__[name].setProperty('visible', True)
            for name in self.ui_items_on_normal_only:
                self.__dict__[name].setProperty('visible', False)
            self.update_print_state_ui()
            self.pgb_printing_progress.setProperty('value',self.printing_progress/100)
            self.lb_printing_progress.setProperty('text', "%d%%"%(self.printing_progress))
            self.lb_printing_filename.setProperty('text',self.printing_filename)
        else:
            for name in self.ui_items_on_printing_only:
                self.__dict__[name].setProperty('visible', False)
            for name in self.ui_items_on_normal_only:
                self.__dict__[name].setProperty('visible', True)
            for name in self.btns_name:
                self.__dict__[name].setProperty('enabled', self.printer_ip != None)
                

    def update_print_state_ui(self):
        self.btn_resume.setProperty('visible', self.is_paused)
        self.btn_pause.setProperty('visible', not self.is_paused)
        self.btn_stop.setProperty('visible', self.is_paused) 
        self.btn_off.setProperty('visible', self.is_paused) 

    def is_ip(self,ip):
        p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        return p.match(ip)

    @pyqtSlot()
    def disconnect_printer(self):
        self.session_id = -1
        self.stop_rolling_state()
        self.txt_printer_ip.setProperty('enabled', True)
        self.btn_connect.setProperty('visible', True)
        self.btn_disconnect.setProperty('visible', False)
        self.reset_state()
        self.update_status()
        self.upload_file_name = None

    def on_session_error(self):
        self.stop_rolling_state()
        self.txt_printer_ip.setProperty('enabled', True)
        self.btn_connect.setProperty('visible', True)
        self.btn_disconnect.setProperty('visible', False)
        self.reset_state()
        self.update_status()

    def reset_state(self):
        self.connect_state = "-1"

        self.is_bed_heating = False
        self.is_nozzle_heating0 = False
        self.is_nozzle_heating1 = False
        self.is_printing = False
        self.is_paused = False

        self.temp_bed_target = 0
        self.temp_bed = 0
        self.temp_nozzle_target0 = 0
        self.temp_nozzle0 = 0
        self.temp_nozzle_target1 = 0
        self.temp_nozzle1 = 0

        self.nozzle_count = 0
        self.current_tool = 0
        self.printing_progress = 0
        self.print_version_code = 0
        self.print_id = 0

        self.printing_filename = ""


    @pyqtSlot()
    def printing_task_pause(self):
        self.btn_pause.setProperty('visible', False)
        self.btn_resume.setProperty('visible', True)
        self.btn_stop.setProperty('visible', True)
        self.send_cmd("pause_print")

    @pyqtSlot()
    def printing_task_resume(self):
        self.btn_pause.setProperty('visible', True)
        self.btn_resume.setProperty('visible', False)
        self.btn_stop.setProperty('visible', False)
        self.send_cmd("resume_print")

    @pyqtSlot()
    def printing_task_stop(self):
        self.send_cmd("stop_print")

    @pyqtSlot()
    def send_gcode(self):
        str_gcode = self.txt_gcode.property("text").strip()
        self.txt_gcode.setProperty("text","")
        if str_gcode and len(str_gcode)>0:
            str_gcode = str_gcode.replace("\r","")
            str_gcode = str_gcode.replace("\\n","\n")
            if str_gcode.find("\n")>=0: #多条
                arr = str_gcode.split("\n")
                for s in arr:
                    if len(s)>0:
                        self.http_send_queue.append({"t":"cmd", "cmd":"gcode", "data":s+"\n"})
            else:
                self.http_send_queue.append({"t":"cmd", "cmd":"gcode", "data":str_gcode+"\n"})
        else:
            logi("Gcode is null")

    @pyqtSlot(str)
    def send_cmd(self,cmd,data=None):
        self.http_send_queue.append({"t":"cmd", "cmd":cmd, "data":data if data else "\n"})

    def query_filelist(self,path = None):
        self.http_send_queue.append({"t":"filelist", "path":path if path else ""})

    @pyqtSlot()
    def show_sd(self):
        self.file_explorer = None
        self.file_explorer_data = []
        self.explorer_selected_index = -1
        self.explorer_cur_dir = ""
        self.file_explorer_model = None

        listView=QListView()
        self.file_explorer_list_view = listView
        listView.setViewMode(QListView.ListMode)
        listView.setIconSize(QSize(16,16))
        listView.setGridSize(QSize(400,24))#每个选项所在网格大小（每个选项外层grid宽高）
        listView.setMinimumHeight(400)#listView最小高度

        listView.setResizeMode(QListView.Adjust)
        listView.setMovement(QListView.Static)

        model=QStandardItemModel()
        listView.setModel(model)
        listView.clicked.connect(self.on_explorer_item_click)
        self.file_explorer_model = model
        
        layout=QVBoxLayout()
        #添加说明：
        lbPath = QLabel("")
        title_group = QHBoxLayout()
        title_group.addWidget(lbPath)
        layout.addLayout(title_group)
        layout.addStretch()

        self.file_explorer_lb_path = lbPath
        layout.addWidget(listView)

        #添加两个按钮
        btn_group = QHBoxLayout()
        layout.addLayout(btn_group)
        btn1 = QPushButton("Delete")
        btn1.clicked.connect(self.on_explorer_delete_click)
        btn_group.addWidget(btn1)
        btn2 = QPushButton("Print")
        btn2.clicked.connect(self.on_explorer_print_click)
        btn_group.addWidget(btn2)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setWindowModality(Qt.ApplicationModal)
        widget.setWindowTitle("Disk - FlyingBear")
        widget.show()
        self.file_explorer = widget

        
        self.upadte_file_explorer(["DSD:","DUSB:"])

    def on_explorer_item_click(self, model_index):
        self.explorer_selected_index = model_index.row()
        logi('你选择了：%d'%(model_index.row()))
        logi(self.file_explorer_data)
        logi(self.explorer_cur_dir)
        name = self.file_explorer_data[self.explorer_selected_index]
        if name[0] == "D":
            self.explorer_cur_dir = os.path.join(self.explorer_cur_dir,name[1:])
            self.file_explorer_lb_path.setText(self.explorer_cur_dir)
            self.query_filelist(self.explorer_cur_dir)
            self.explorer_selected_index == -1
            self.file_explorer_list_view.setVisible(False)
        if name[0] == "B":
            if self.explorer_cur_dir == "SD:" or self.explorer_cur_dir == "USB:":
                self.upadte_file_explorer(["DSD:","DUSB:"])
                self.explorer_cur_dir = ""
                self.file_explorer_lb_path.setText(self.explorer_cur_dir)
            else:
                self.explorer_cur_dir = os.path.dirname(self.explorer_cur_dir)
                logi(self.explorer_cur_dir)
                self.file_explorer_lb_path.setText(self.explorer_cur_dir)
                self.query_filelist(self.explorer_cur_dir)
                self.explorer_selected_index == -1
                self.file_explorer_list_view.setVisible(False)

    def on_explorer_delete_click(self):
        if self.explorer_selected_index != -1 and self.explorer_selected_index < len(self.file_explorer_data):
            name = self.file_explorer_data[self.explorer_selected_index]
            if name[0] == "F":
                self.send_cmd("delete_file", os.path.join(self.explorer_cur_dir,name[1:]))
                self.file_explorer_model.removeRow(self.explorer_selected_index)
                self.file_explorer_data.remove(name)
                # if self.explorer_selected_index >= len(self.file_explorer_data):
                #     self.explorer_selected_index = len(self.file_explorer_data)-1
                # if self.explorer_selected_index>=0:
                #     self.file_explorer_list_view.setCurrentRow(self.explorer_selected_index)
                self.explorer_selected_index = -1
            else:
                logi("不能删除")

    def on_explorer_print_click(self):
        if self.explorer_selected_index != -1 and self.explorer_selected_index < len(self.file_explorer_data):
            name = self.file_explorer_data[self.explorer_selected_index]
            if name[0] == "F":
                self.send_cmd("print_start", os.path.join(self.explorer_cur_dir,name[1:]))
                self.file_explorer.close()
            else:
                logi("不能打印")

    def upadte_file_explorer(self,arr):
        self.file_explorer_data = arr
        model = self.file_explorer_model
        model.clear()

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res")
        for name in arr:
            icon = ""
            if name[0] == "D":
                icon = os.path.join(path,"folder.png")
            elif name[0] == "B":
                icon = os.path.join(path,"arrow_left.png")

            item = QStandardItem(QIcon(icon), name[1:])
            item.setEditable(False)
            model.appendRow(item)
    
    @pyqtSlot()
    def show_upload(self):
        openfile_path,_ = QFileDialog.getOpenFileName(None,'Choose File',self.last_upload_dir if self.last_upload_dir else ''
            ,'All Files (*);;Gcode files(*.gco);;Gcode files(*.gcode);;Gcode files(*.gjz);;Bin files(*.bin)')
        if openfile_path and len(openfile_path)>0:
            self.last_upload_dir = os.path.dirname(openfile_path)
            self.save_user_data()
            self.showDialogUploading(openfile_path)

    def on_upload_progress(self, bytesSent, bytesTotal):
        logi("upload %d/%d "%(bytesSent, bytesTotal))
        rate = 0
        if bytesTotal>0:
            self.upload_sent_size = bytesSent
            self.upload_total_size = bytesTotal
            rate = bytesSent/bytesTotal
            speed = bytesSent/(time.time()-self.upload_start_time)
            self.dialog_uploading_ui["pgb_progress"].setProperty('value', rate)
            self.dialog_uploading_ui["lb_speed"].setProperty('text', 'Speed: %.2fK/S' % (speed/1024))
            self.dialog_uploading_ui["lb_remain_time"].setProperty('text', 'Remain Time: %d Second' % (int((bytesTotal-bytesSent)/speed)))
            self.dialog_uploading.setProperty('title', 'Progress  %d%%' % (int(rate*100)))
        
    def on_upload_result(self, http_req, reply):
        reply_body = bytes(reply.readAll()).decode()
        if reply_body != None and len(reply_body)>0:
            logi( reply_body)
            if reply_body.find("{") >= 0:
                obj = json.loads(reply_body)
                if obj["c"] == 0:
                    start_printing = self.dialog_uploading_ui["ck_auto_start_print"].property('checked')
                    if start_printing:
                        self.send_cmd("print_start", self.upload_file_save_path)
                    else:
                        Message(os.path.basename(self.upload_file_path) +" is uploaded to your printer!", lifetime = 8).show()
                else:
                    code = obj["c"]
                    logi("Error code=%d msg=%s"%(obj["c"], obj["m"]))
                    if code == 7 or code==8:
                        Message(obj["m"], lifetime = 8).show()

        self.dialog_uploading.hide()
        self.upload_http_request = None
        self.is_uploading = False

    def on_upload_error(self, http_req, errorCode):
        logi( "network error code=%d url=%s" % (errorCode,http_req.url))
        self.dialog_uploading.hide()
        if errorCode == QtNetwork.QNetworkReply.OperationCanceledError:
            Message("%s transfer canceled!"%(os.path.basename(self.upload_file_path)), lifetime = 8).show()
        else:
            Message("%s transfer failed!"%(os.path.basename(self.upload_file_path)), lifetime = 8).show()

    def start_upload(self,save_path,file_path):
        self.upload_file_path = file_path
        self.upload_file_save_path = save_path
        self.is_uploading = True
        data = QByteArray()
        with open(file_path, 'rb') as f:
            data.append(f.read())

        self.upload_start_time = time.time()
        self.upload_http_request = HttpRequest(self,"http://%s/upload"%(self.printer_ip),{},self.on_upload_result,self.on_upload_error, data, self.on_upload_progress)
        self.upload_http_request.set_header("path", save_path)
        self.upload_http_request.run()
        self.dialog_uploading_ui["lb_uploading_filename"].setProperty('text', "Filename: "+os.path.basename(file_path))

    @pyqtSlot()
    def connect_printer(self):
        if self.delay_auto_connect_timer:
            self.delay_auto_connect_timer.stop()
            self.delay_auto_connect_timer = None

        ip = self.txt_printer_ip.property('text').strip()
        if len(ip)>0 and self.is_ip(ip) and not self.cur_http_request:
            http_request = HttpRequest(self,"http://%s/connect"%(ip),{"ip":ip},self.on_connect_result,self.on_connect_error)
            http_request.set_timeout(5)
            http_request.run()
            self.cur_http_request = http_request

    def on_connect_result(self, http_request, reply):
        self.cur_http_request = None
        reply_body = bytes(reply.readAll()).decode()
        if reply_body != None and len(reply_body)>0:
            logi( reply_body)
            if reply_body.find("{") >= 0:
                obj = json.loads(reply_body)
                if obj["c"] == 0:
                    self.session_id = obj["m"]
                    self.printer_ip = http_request.para.get("ip")
                    self.last_ip = self.printer_ip
                    self.save_user_data()
                    self.start_rolling_state()
                    self.txt_printer_ip.setProperty('enabled', False)
                    self.btn_connect.setProperty('visible', False)
                    self.btn_disconnect.setProperty('visible', True)

                    if self.upload_file_name:
                        self.showDialogUploading(self.upload_file_name)
                    self.upload_file_name = None

                    if self.printer_ip not in self.ip_list:
                        self.ip_list.append(self.printer_ip)
                        self.save_user_data()
                        self.update_history_ip()
                else:
                    logi("Error code=%d msg=%s"%(obj["c"], obj["m"]))
    
    def on_connect_error(self, http_request, errorCode):
        message = Message(("Connection Failed!"), lifetime = 5)
        message.show()
        self.lb_printer_state.setProperty("text","Connection Failed!")


    def on_query_status_result(self, http_request, reply):
        self.cur_http_request = None
        if self.session_id == -1: #网络请求回来前，用户点了断开连接，则丢弃结果
            return
        reply_body = bytes(reply.readAll()).decode("gbk")
        if reply_body != None and len(reply_body)>0:
            logi(reply_body)
            if reply_body.find("DATA") == 0:
                reply_body = reply_body[4:]
                status = reply_body.split(",")
                if len(status) == 18:
                    self.connect_state = status[0]

                    self.is_bed_heating = status[1] == "1"
                    self.is_nozzle_heating0 = status[2] == "1"
                    self.is_nozzle_heating1 = status[3] == "1"
                    self.is_printing = status[4] == "1"
                    self.is_paused = status[5] == "1"

                    self.temp_bed_target = int(status[6])
                    self.temp_bed = int(status[7])
                    self.temp_nozzle_target0 = int(status[8])
                    self.temp_nozzle0 = int(status[9])
                    self.temp_nozzle_target1 = int(status[10])
                    self.temp_nozzle1 = int(status[11])

                    self.nozzle_count = int(status[12])
                    self.current_tool = int(status[13])
                    self.printing_progress = int(status[14])
                    self.print_version_code = int(status[15])
                    self.print_id = int(status[16])
                    if self.is_printing:
                        self.printing_filename = status[17] 
                    else:
                        self.printing_filename = ""

                    self.update_status()
            elif reply_body.find("{") >= 0:
                obj = json.loads(reply_body)
                if obj["c"] == 99:
                    self.on_session_error()
                else:
                    logi("Error code=%d msg=%s"%(obj["c"], obj["m"]))

    def on_cmd_result(self, http_request, reply):
        self.cur_http_request = None   
        reply_body = bytes(reply.readAll()).decode("gbk")
        if reply_body != None and len(reply_body)>0:
            logi( reply_body)
            if reply_body.find("{") >= 0:
                obj = json.loads(reply_body)
                if obj["c"] == 0:
                    if http_request.cmd == "gcode":
                        message = Message("Gcode [%s] sent successfully!"%(http_request.cmd_data.replace("\n","")), lifetime = 8)
                        message.show()
                    elif http_request.cmd == "delete_file":
                        logi("delete file succ")
                    else:
                        logi("on_cmd_result: %s"%(obj["m"]))
                else:
                    logi("Error code=%d msg=%s"%(obj["c"], obj["m"]))

    def on_filelist_result(self, http_request, reply):
        self.cur_http_request = None   
        reply_body = bytes(reply.readAll()).decode("gbk")
        if reply_body != None and len(reply_body)>0:
            logi(reply_body)
            if reply_body[len(reply_body)-1] == "\n":
                reply_body = reply_body[0:-1]
            if reply_body == "R":
                self.explorer_selected_index = -1
                self.explorer_cur_dir = ""
                self.file_explorer_lb_path.setText(self.explorer_cur_dir)
                self.upadte_file_explorer(["DSD:","DUSB:"])
            else:
                arr = reply_body.split("\n")
                if arr[0] == "R":
                    arr.pop(0)
                
                arr_sorted = []
                arr_sorted.insert(0,"BBack")
                arr_files = []
                for name in arr:
                    if name[0] == "D":
                        arr_sorted.append(name)
                    else:
                        arr_files.append(name)
                arr_sorted.extend(arr_files)
                self.upadte_file_explorer(arr_sorted)
        self.file_explorer_list_view.setVisible(True)

    def on_http_error(self, http_request, errorCode):
        logi( "network error code=%d url=%s" % (errorCode,http_request.url))

    def do_rolling(self):
        #{"t":"cmd","cmd":"gcode","data":s+"\n"}
        if self.printer_ip!= None and self.upload_http_request == None and self.cur_http_request == None:
            try:
                if len(self.http_send_queue) > 0:
                    req = self.http_send_queue.pop(0)
                    t = req.get("t")
                    if t == "cmd":
                        cmd = req.get("cmd")
                        data = req.get("data")
                        http_request = HttpRequest(self,"http://%s/cmd"%(self.printer_ip),{},self.on_cmd_result,self.on_http_error)
                        http_request.set_header("cmd", cmd)
                        http_request.set_request_info(t,cmd,data)
                        if data:
                            http_request.set_data(data.encode('gbk'))
                        #http_request.set_timeout(5)
                        self.cur_http_request = http_request
                        http_request.run()
                    elif t == "filelist":
                        data = req.get("path")
                        http_request = HttpRequest(self,"http://%s/filelist"%(self.printer_ip),{},self.on_filelist_result,self.on_http_error)
                        http_request.set_request_info(t,None,data)
                        if data:
                            http_request.set_data(data.encode('gbk'))
                        #http_request.set_timeout(5)
                        self.cur_http_request = http_request
                        http_request.run()
                    else:
                        Logger.i("i","Unknow request %s"%(req))
                else:
                    if time.time() - self.last_get_status_time >=1:
                        self.last_get_status_time = time.time()
                        http_request = HttpRequest(self,"http://%s/status"%(self.printer_ip),{},self.on_query_status_result,self.on_http_error)
                        http_request.set_request_info("status",None,None)
                        #http_request.set_timeout(5)
                        self.cur_http_request = http_request
                        http_request.run()

            except Exception as e:
                self.cur_http_request = None
                Logger.log("i",e)
        else:
            pass
            #logi("not do_rolling %s %s %s"%(str(self.printer_ip!= None), str(self.upload_http_request == None), str( self.cur_http_request == None)))

    def start_rolling_state(self):
        if self.timer:
            self.timer.stop()
        self.timer = QTimer()
        self.timer.timeout.connect(self.do_rolling)
        self.timer.start(100)

    def stop_rolling_state(self):
        if self.timer:
            self.timer.stop()
            self.timer = None
        self.printer_ip = None

    def exit(self):
        self.stop_rolling_state()