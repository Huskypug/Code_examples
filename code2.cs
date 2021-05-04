        private void Report1()
        {
            while (!reportCancelFlag)
            {
                try
                {
                    if (device != null)// && device.IsConnected && device.IsOpen)
                    {
                        HidReport rep = device.ReadReport();
                        if (rep.ReportId != 5)
                        {
                            Thread CalcThread = new Thread(() => { OnReport(rep); });
                            CalcThread.IsBackground = true;
                            CalcThread.Name = "CalcThread";
                            CalcThread.Start();
                            
                        }
                        Thread.Sleep(10);
                    }
                }
                catch
                {
                    MessageBox.Show("Data loss");
                }

            }
        }
        private void OnReport(HidReport report)
        {
            DateTime timestamp = DateTime.Now;
            if (report != null && report.Data.Length != 0)
            {

                switch (report.ReportId)
                {
                    case 1:         //Raw ADC Data
                        float[] floats = new float[20];
                        for (int i = 0; i < 20; i++)
                        {
                            floats[i] = BitConverter.ToSingle(report.Data, i * 4);
                        }

                        RawADCRecievedEvent?.Invoke(this, new RawADCRecievedEventArgs(floats, timestamp));
                        break;
                    case 2:         //5 pixel device
                                    //struct {
                                    //  byte reportID = 2,
                                    //  int pointNum, //different pointNum for different samples
                                    ////  float[5] Isd
                                    //  float[5] Vsg
                                    //}

                        int pointNum = BitConverter.ToInt32(report.Data, 0);
                        App prj = (App)Application.Current;
                        lock (prj)
                        {
                            bool projectexists = true;
                            if (prj.CurrentProject == null)
                            {
                                if (prj.Projects.Count == 0)
                                {
                                    projectexists = false;
                                    var projectname = string.Format("Project {0:dd.MM.yy HH.mm.ss}", DateTime.Now);
                                    var proj = new Project(projectname);
                                    proj.TimeStamp = DateTime.Now;
                                    for (int i = 0; i < 5; i++)
                                    {
                                        Pixel pixel = new Pixel(proj, i);
                                        proj.Pixels.Add(pixel);

                                    }
                                    Pixel_aux pixel_aux = new Pixel_aux(proj, "Common data");
                                    proj.Pixel_Aux = pixel_aux;
                                    Application.Current.Dispatcher.Invoke(delegate
                                    {
                                        prj.Projects.Add(proj);
                                    });
                                    prj.CurrentProject = proj;
                                }
                                prj.CurrentProject = prj.Projects.Last();
                            }
                            if (((pointNum != lastCurveId) || !projectexists))
                            {
                                //FS = true;
                                for (int i = 0; i < 5; i++)
                                {

                                    DateTime now = DateTime.Now;
                                    ParametricCurve Local_curve = new ParametricCurve();
                                    Local_curve.Pixel = prj.CurrentProject.Pixels[i];
                                    Local_curve.SampleName = (prj.CurrentProject.Pixels[i].Curves.Count).ToString() + " " + (now).ToString("HH.mm.ss");
                                    prj.CurrentProject.Pixels[i].Curves.Add(Local_curve);
                                    CurveRecievedEvent?.Invoke(this, new CurveRecievedEventArgs(prj.CurrentProject.Pixels[i].Curves.Last(), i, 5));


                                }
                                ParametricCurve_aux aux1 = new ParametricCurve_aux();
                                int time_temp = (int)Math.Round((DateTime.Now - prj.CurrentProject.TimeStamp).TotalMilliseconds, 0);
                                aux1.Tmax = time_temp.ToString();
                                aux1.Concentration = "0";
                                aux1.Pixel_aux = prj.CurrentProject.Pixel_Aux;
                                aux1.SampleName = (prj.CurrentProject.Pixel_Aux.Curves.Count).ToString();
                                if (prj.CurrentProject.Pixel_Aux.Curves.Count > 0)
                                {
                                    aux1.Concentration = prj.CurrentProject.Pixel_Aux.Curves.Last().Concentration;
                                }
                                lastCurveId = pointNum;

                            }
                            DispRecievedEvent?.Invoke(this, new DisplayRecievedEventArgs("Measuring"));


                            uint millisFromStart = BitConverter.ToUInt32(report.Data, 44);
                            float Rh = BitConverter.ToSingle(report.Data, 48);
                            float Temp = BitConverter.ToSingle(report.Data, 52);

                            OFETDataPoint point_aux20 = new OFETDataPoint(Rh, Temp)//, -42, 0, Vsg, 0, Rh, Temp)
                            {
                                TS = millisFromStart,//measureStartTime.AddMilliseconds(millisFromStart),//timestamp
                            };
                            curve_aux20.Points.Add(point_aux20);
                            ParametricCurve_aux aux = prj.CurrentProject.Pixel_Aux.Curves.Last();
                            aux.Points.Add(point_aux20);
                            aux.Points.Last().Isd = -1.0;
                            aux.Rh = Rh.ToString();
                            aux.airTemp = Temp.ToString();


                            for (int i = 0; i < 5; i++)
                            {
                                float Isd = BitConverter.ToSingle(report.Data, 4 + i * 4);
                                float Vsd = BitConverter.ToSingle(report.Data, 26);
                                float Vsg = BitConverter.ToSingle(report.Data, 22);
                                OFETDataPoint point = new OFETDataPoint(Vsd,Isd, Vsg);
                                if (Isd > prj.CurrentProject.Pixels[i].Scatter_Max)
                                    prj.CurrentProject.Pixels[i].Scatter_Max = Isd;
                                prj.CurrentProject.Pixels[i].Curves.Last().Points.Add(point);
                                if (i == 4) PointRecievedEvent?.Invoke(this, new PointRecievedEventArgs(prj.CurrentProject.Pixels[i].Curves.Last()));
                            }
                        }

                        break;
                    case 3:         //20 pixel device
                                    //struct {
                                    //  byte reportID = 2,
                                    //  int pointNum, //different pointNum for different samples
                                    ////  float[5] Isd
                                    //  float[5] Vsg
                                    //}
                        int pointNum20 = BitConverter.ToInt16(report.Data, 0);
                        int grouptag = report.Data[2];
                        prj = (App)Application.Current;
                        lock (prj)
                        {
                            bool projectexists = true;
                            if (prj.CurrentProject == null)
                            {
                                if (prj.Projects.Count == 0)
                                {
                                    projectexists = false;
                                    var projectname = string.Format("Project {0:dd.MM.yy HH.mm.ss}", DateTime.Now);
                                    var proj = new Project(projectname);
                                    proj.TimeStamp = DateTime.Now;
                                    for (int i = 0; i < 20; i++)
                                    {
                                        Pixel pixel = new Pixel(proj, i);
                                        proj.Pixels.Add(pixel);

                                    }
                                    Pixel_aux pixel_aux = new Pixel_aux(proj, "Common data");
                                    proj.Pixel_Aux = pixel_aux;
                                    Application.Current.Dispatcher.Invoke(delegate
                                    {
                                        prj.Projects.Add(proj);
                                    });
                                    prj.CurrentProject = proj;
                                }
                                prj.CurrentProject = prj.Projects.Last();
                            }
                            if (((pointNum20 != lastCurveId) || !projectexists))
                            {
                                for (int i = 0; i < 20; i++)
                                {
                                    //curves[i].Sort();
                                    //curves[i].Points.Clear();

                                    DateTime now = DateTime.Now;
                                    ParametricCurve Local_curve = new ParametricCurve();
                                    Local_curve.Pixel = prj.CurrentProject.Pixels[i];
                                    Local_curve.SampleName = (prj.CurrentProject.Pixels[i].Curves.Count).ToString() + " " + (now).ToString("HH.mm.ss");
                                    prj.CurrentProject.Pixels[i].Curves.Add(Local_curve);
                                    CurveRecievedEvent?.Invoke(this, new CurveRecievedEventArgs(prj.CurrentProject.Pixels[i].Curves.Last(), i, 20));
                                }
                                ParametricCurve_aux aux1 = new ParametricCurve_aux();
                                int time_temp = (int)Math.Round((DateTime.Now - prj.CurrentProject.TimeStamp).TotalMilliseconds, 0);
                                aux1.Tmax = time_temp.ToString();
                                aux1.Pixel_aux = prj.CurrentProject.Pixel_Aux;
                                aux1.Concentration = "0";
                                aux1.SampleName = (prj.CurrentProject.Pixel_Aux.Curves.Count).ToString();
                                if (prj.CurrentProject.Pixel_Aux.Curves.Count > 0)
                                {
                                    aux1.Concentration = prj.CurrentProject.Pixel_Aux.Curves.Last().Concentration;
                                }
                                prj.CurrentProject.Pixel_Aux.Curves.Add(aux1);

                                lastCurveId = pointNum20;
                            }
                            if (grouptag == 1)
                            {
                                uint millisFromStart = BitConverter.ToUInt32(report.Data, 3);

                                float Rh = (float)report.Data[56] + (float)(report.Data[55]) / 100;//BitConverter.ToSingle(report.Data, 56);
                                float airTemp = (float)report.Data[58] + (float)(report.Data[57]) / 100;// BitConverter.ToSingle(report.Data, 57);
                                float sampleTemp = (float)report.Data[60] + (float)(report.Data[59]) / 100;// BitConverter.ToSingle(report.Data, 57);

                                OFETDataPoint point_aux = new OFETDataPoint(Rh, airTemp)
                                {
                                    TS = millisFromStart,
                                };
                                curve_aux.Points.Add(point_aux);
                                ParametricCurve_aux aux = prj.CurrentProject.Pixel_Aux.Curves.Last();
                                aux.Points.Add(point_aux);
                                aux.Points.Last().Isd = -1.0;
                                aux.Rh = Rh.ToString();
                                aux.airTemp = airTemp.ToString();
                                aux.sampleTemp = sampleTemp.ToString();
                                RhTempRecievedEvent?.Invoke(this, new RhTempRecievedEventArgs(Math.Round(Rh, 2), Math.Round(airTemp, 2), Math.Round(sampleTemp, 2)));
                                DispRecievedEvent?.Invoke(this, new DisplayRecievedEventArgs("Measuring"));
                            }
                            for (int i = (grouptag - 1) * 10; i < 10 * grouptag; i++)
                            {
                                float Isd = 0;
                                float Vsg20 = BitConverter.ToSingle(report.Data, 47);
                                float Vsd20 = BitConverter.ToSingle(report.Data, 51);
                                if (grouptag == 1) Isd = BitConverter.ToSingle(report.Data, 7 + i * 4);
                                if (grouptag == 2) Isd = BitConverter.ToSingle(report.Data, 7 + (i - 10) * 4);
                                OFETDataPoint point = new OFETDataPoint(Vsd20,Isd,Vsg20);
                                if (Isd > prj.CurrentProject.Pixels[i].Scatter_Max)
                                    prj.CurrentProject.Pixels[i].Scatter_Max = Isd;
                                prj.CurrentProject.Pixels[i].Curves.Last().Points.Add(point);
                                //curves[i].Points.Add(point);
                                if (i == 19) PointRecievedEvent?.Invoke(this, new PointRecievedEventArgs(prj.CurrentProject.Pixels[i].Curves.Last()));
                            }

                        }
                        break;
                    case 6:
                        String log1 = Encoding.UTF8.GetString(report.Data);
                        log1 = log1.Replace((char)0,' ');
                        prj = (App)Application.Current;
                        if (prj.CurrentProject != null)
                            prj.CurrentProject.Comments += log1 + "\n";
                        LogRecievedEvent?.Invoke(this, new LogRecievedEventArgs(log1));
                        break;
                    case 7:

                        break;
                    case 8: // if datacount < 59 stop getting data; get options
                        if (OptionsBytes == null)
                        {
                            if (Id == 22352)
                                OptionsBytes = new byte[308];
                            if (Id == 22354)
                                OptionsBytes = new byte[544];
                        }
                        int offset = BitConverter.ToUInt16(report.Data, 0);//report.Data[0];
                        int datacount = report.Data[2];
                        Array.Copy(report.Data, 3, OptionsBytes, offset, datacount);


#if DEBUG
                        Debug.Write("Recv: " + BitConverter.ToString(OptionsBytes) + "\n");
#endif
                        if (datacount < 58)
                            OptionsRecievedEvent?.Invoke(this, new OptionsRecievedEventArgs(OptionsBytes));
                        break;
                    case 9:
                        break;
                    case 10:
                        String Dispraw = Encoding.UTF8.GetString(report.Data,0,32);
                        String selected_option = Dispraw.Split(new[] { "\0" }, StringSplitOptions.None)[0];
                        DispRecievedEvent?.Invoke(this, new DisplayRecievedEventArgs(selected_option));
                        break;
                    case 11:
                        Status = report.Data[0];
                        if (Status == 1)
                        {
                            DispRecievedEvent?.Invoke(this, new DisplayRecievedEventArgs("Resting"));
                            CurveRecievedEvent?.Invoke(this, new CurveRecievedEventArgs(null, 0, 0));
                            LastEnd = DateTime.Now;
                            
                        }
                        break;
                    default:

                        break;

                }
            }
        }