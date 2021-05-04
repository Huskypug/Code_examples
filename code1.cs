public static object DeserializeAs5(string jsonString, Type targetType)
        {
            JObject o = JObject.Parse(jsonString);
            Project pr = null;
            if (o.SelectToken("Comments") != null)
                {
                pr = new Project
                {
                    Name = (String)o.SelectToken("Name"),
                    TimeStamp = (DateTime)o.SelectToken("TimeStamp"),
                    Comments = (String)o.SelectToken("Comments")
                    
                };
            }
            else
            {
                pr = new Project
                {
                    Name = (String)o.SelectToken("Name"),
                    TimeStamp = (DateTime)o.SelectToken("TimeStamp")
                };
            }
            pr.Pixel_Aux = new Pixel_aux(pr, "Common data");

            //Get timeSplit for points in Curve
            double Time_split = 0;
            int Time_cnt = 0;
            for (int d = 0; d< 10; d++)
            {
                if (Time_split != 0)
                    break;
                JArray points_count = (JArray)o.SelectToken("Pixel_Aux.Curves[" + Time_cnt.ToString() + "].Points");
                if (points_count != null)
                {
                    if (points_count.Count > 1)
                    {
                        if (o.SelectToken("Pixel_Aux.Curves[" + Time_cnt.ToString() + "].Points[0].TS") != null)
                        {
                            Time_split = (double)o.SelectToken("Pixel_Aux.Curves[" + Time_cnt.ToString() + "].Points[1].TS") - (double)o.SelectToken("Pixel_Aux.Curves[" + Time_cnt.ToString() + "].Points[0].TS");
                        }
                        if (o.SelectToken("Pixel_Aux.Curves[" + Time_cnt.ToString() + "].Points[0].Timestamp") != null)
                        {
                            Time_split = (double)o.SelectToken("Pixel_Aux.Curves[" + Time_cnt.ToString() + "].Points[1].Timestamp") - (double)o.SelectToken("Pixel_Aux.Curves[" + Time_cnt.ToString() + "].Points[0].Timestamp");
                        }

                    }
                }
                
                Time_cnt++;
            }
            



            JArray Pcnt = (JArray)o.SelectToken("Pixels");
            for (int i = 0; i < Pcnt.Count; i++)
            {
                string rej = (String)o.SelectToken("Pixels[" + i.ToString() + "].Rejected");
                if (rej != null)
                {
                    Pixel pixel = new Pixel(pr, (int)o.SelectToken("Pixels[" + i.ToString() + "].PixelNumber"))
                    {
                        Rejected = bool.Parse(rej),
                        Project = pr,
                        BaseLine = (double)o.SelectToken("Pixels[" + i.ToString() + "].BaseLine")
                    };
                    pr.Pixels.Add(pixel);
                }
                else
                    continue;

                JArray Ccnt = (JArray)o.SelectToken("Pixel_Aux.Curves");
                for (int j = 0; j < Ccnt.Count; j++)
                {
                    ParametricCurve curve = new ParametricCurve()
                    {
                        SampleName = (String)o.SelectToken("Pixels[" + i.ToString() + "]._Curves[" + j.ToString() + "].SampleName"),
                        Pixel = pr.Pixels[i]

                    };
                    pr.Pixels[i].Curves.Add(curve);
                    if (i == 0)
                    {
                        ParametricCurve_aux curve_Aux = new ParametricCurve_aux();
                        curve_Aux.Tmax = (String)o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Tmax");
                        curve_Aux.Pixel_aux = pr.Pixel_Aux;
                        curve_Aux.Concentration = (String)o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Concentration");
                        if (o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].airTemp") != null)
                            curve_Aux.airTemp = (String)o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].airTemp");
                        if (o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Temp") != null)
                            curve_Aux.airTemp = (String)o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Temp");
                        curve_Aux.sampleTemp = (String)o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].sampleTemp");
                        curve_Aux.Rh = (String)o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Rh");
                        curve_Aux.SampleName = (String)o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].SampleName");
                        curve_Aux.Comments = (String)o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Comments");
                        curve_Aux.Rejected = (bool)o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Rejected");
                        pr.Pixel_Aux.Curves.Add(curve_Aux);
                    }
                    //Aux
                    JArray Pocnt = (JArray)o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Points");
                    if (Pocnt != null)
                    {
                        for (int k = 0; k < Pocnt.Count; k++)
                        {
                            if (i == 0)//only one for points
                            {
                                if (Pocnt.Count > 0)
                                {
                                    
                                    OFETDataPoint point_aux = new OFETDataPoint(-1.0);//, -42, 0, -40, 0, (double)o.SelectToken("pixels[" + i.ToString() + "].Curves[" + j.ToString() + "].Points[" + k.ToString() + "].rh"), (double)o.SelectToken("pixels[" + i.ToString() + "].Curves[" + j.ToString() + "].Points[" + k.ToString() + "].temp"))
                                    if (o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Points[" + k.ToString() + "].TS") != null)
                                    {
                                        point_aux.TS = (double)o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Points[" + k.ToString() + "].TS");
                                    }
                                    if (o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Points[" + k.ToString() + "].Timestamp") != null)
                                    {
                                        point_aux.TS = (double)o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Points[" + k.ToString() + "].Timestamp");
                                    }
                                    if (k > 0)
                                        if (pr.Pixel_Aux.Curves[j].Points.Last().TS != point_aux.TS)
                                            pr.Pixel_Aux.Curves[j].Points.Add(point_aux);
                                    if (k == 0)
                                        pr.Pixel_Aux.Curves[j].Points.Add(point_aux);
                                }
                            }
                        }
                    }
                    //Normal
                     Pocnt = (JArray)o.SelectToken("Pixels[" + i.ToString() + "]._Curves[" + j.ToString() + "].Points");
                    if (Pocnt != null)
                    {
                        for (int k = 0; k < Pocnt.Count; k++)
                        {
                            if (i == 0)//only one for points
                            {
                                if (k > pr.Pixel_Aux.Curves[j].Points.Count - 1 && k > 0)
                                {
                                    OFETDataPoint point_aux = new OFETDataPoint(-1.0);//, -42, 0, -40, 0, (double)o.SelectToken("pixels[" + i.ToString() + "].Curves[" + j.ToString() + "].Points[" + k.ToString() + "].rh"), (double)o.SelectToken("pixels[" + i.ToString() + "].Curves[" + j.ToString() + "].Points[" + k.ToString() + "].temp"))
                                    if (o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Points[" + (k - 1).ToString() + "].TS") != null)
                                    {
                                        point_aux.TS = (double)o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Points[" + (k - 1).ToString() + "].TS") + Time_split;
                                    }
                                    if (o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Points[" + (k - 1).ToString() + "].Timestamp") != null)
                                    {
                                        point_aux.TS = (double)o.SelectToken("Pixel_Aux.Curves[" + j.ToString() + "].Points[" + (k - 1).ToString() + "].Timestamp") + Time_split;
                                    }
                                    pr.Pixel_Aux.Curves[j].Points.Add(point_aux);
                                }
                            }
                            OFETDataPoint point = new OFETDataPoint((double)o.SelectToken("Pixels[" + i.ToString() + "]._Curves[" + j.ToString() + "].Points[" + k.ToString() + "].Isd"))//, -42, 0, -40, 0, (double)o.SelectToken("pixels[" + i.ToString() + "].Curves[" + j.ToString() + "].Points[" + k.ToString() + "].rh"), (double)o.SelectToken("pixels[" + i.ToString() + "].Curves[" + j.ToString() + "].Points[" + k.ToString() + "].temp"))
                            {
                            };
                            pr.Pixels[i].Curves[j].Points.Add(point);
                            if (pr.Pixels[i].Curves[j].Points.Count > 0)
                            {
                                double local_max = pr.Pixels[i].Curves[j].Points.Max(m => m.Isd);
                                if (local_max > pr.Pixels[i].Scatter_Max)
                                    pr.Pixels[i].Scatter_Max = local_max;
                            }

                        }
                    }
                        

                }
            }
            return pr;
        }