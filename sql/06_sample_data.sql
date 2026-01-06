-- =============================================
-- 06_sample_data.sql
-- FULL SAMPLE DATA (COPY)
-- =============================================

-- -----------------------------
-- KATEGORI
-- -----------------------------
COPY public.kategori (kategoriid, kategoriadi) FROM stdin;
1	Roman
2	Bilim
3	Tarih
4	Bilgisayar
5	Felsefe
6	Psikoloji
7	Edebiyat
8	Eğitim
9	Mühendislik
10	Kişisel Gelişim
11	Sanat
12	Sosyoloji
13	Hukuk
14	Ekonomi
15	Matematik
16	Fizik
17	Kimya
18	Biyoloji
19	Çocuk
20	Gençlik
\.


-- -----------------------------
-- KULLANICI
-- -----------------------------
COPY public.kullanici (kullaniciid, kullaniciadi, sifre, rol) FROM stdin;
6	admin	Admin@123	Admin
7	yonetici	Yonetici2025	Admin
8	gorevli_yasin	Yasin12345	Gorevli
9	gorevli_engin	Engin!789	Gorevli
\.


-- -----------------------------
-- UYE
-- -----------------------------
COPY public.uye (uyeid, ad, soyad, email, telefon, toplamborc) FROM stdin;
1	Ahmet	Yılmaz	ahmet.yilmaz@mail.com	05551230001	0.00
2	Ayşe	Demir	ayse.demir@mail.com	05551230002	0.00
3	Mehmet	Kaya	mehmet.kaya@mail.com	05551230003	0.00
4	Elif	Çelik	elif.celik@mail.com	05551230004	0.00
5	Can	Şahin	can.sahin@mail.com	05551230005	0.00
6	Zeynep	Koç	zeynep.koc@mail.com	05551230006	0.00
7	Murat	Aydın	murat.aydin@mail.com	05551230007	0.00
8	Buse	Öztürk	buse.ozturk@mail.com	05551230008	0.00
9	Emre	Arslan	emre.arslan@mail.com	05551230009	0.00
10	Selin	Doğan	selin.dogan@mail.com	05551230010	0.00
12	Hakan	Şimşek	hakan.simsek@mail.com	05551230111	0.00
13	Selma	Yıldırım	selma.yildirim@mail.com	05551230112	0.00
14	Burak	Özcan	burak.ozcan@mail.com	05551230113	0.00
15	Merve	Aksoy	merve.aksoy@mail.com	05551230114	0.00
16	Onur	Kurt	onur.kurt@mail.com	05551230115	0.00
17	Derya	Polat	derya.polat@mail.com	05551230116	0.00
18	Kerem	Güneş	kerem.gunes@mail.com	05551230117	0.00
19	İrem	Şen	irem.sen@mail.com	05551230118	0.00
20	Tolga	Eren	tolga.eren@mail.com	05551230119	0.00
21	Nazlı	Karaca	nazli.karaca@mail.com	05551230120	0.00
22	Yasin	Engin	yasin.engin@gmail.com	4545454545	0.00
\.


-- -----------------------------
-- KITAP
-- -----------------------------
COPY public.kitap (kitapid, kitapadi, yazar, yayinevi, basimyili, kategoriid, toplamadet, mevcutadet) FROM stdin;
1	Kürk Mantolu Madonna	Sabahattin Ali	Yapı Kredi	2019	1	12	12
2	Tutunamayanlar	Oğuz Atay	İletişim	2020	1	8	8
3	1984	George Orwell	Can Yayınları	2021	1	15	14
4	Suç ve Ceza	Dostoyevski	İş Bankası	2018	10	10	10
5	Bilgisayar Ağları	Andrew S. Tanenbaum	Pearson	2020	4	6	6
6	Operating System Concepts	Silberschatz	Wiley	2019	4	5	5
7	Clean Code	Robert C. Martin	Prentice Hall	2017	4	9	9
8	Design Patterns	GoF	Addison-Wesley	2016	4	4	4
9	Digital Design	M. Morris Mano	Pearson	2018	9	7	7
10	Signals and Systems	Alan V. Oppenheim	Pearson	2019	9	6	5
11	Nutuk	Mustafa Kemal Atatürk	Türk Tarih Kurumu	2015	3	20	20
12	Osmanlı Tarihi	Halil İnalcık	Kronik	2020	3	10	10
13	Devlet	Platon	İş Bankası	2016	5	8	8
14	Varlık ve Hiçlik	Jean-Paul Sartre	Can Yayınları	2017	5	5	5
15	İnsan Olmak	Engin Geçtan	Metis	2018	6	9	9
16	Duygusal Zeka	Daniel Goleman	Varlık	2020	6	11	11
17	Eğitim Psikolojisi	Anita Woolfolk	Pearson	2019	8	6	6
18	Öğretimde Planlama	Doğan Cüceloğlu	Remzi	2018	8	7	7
19	Atomik Alışkanlıklar	James Clear	Pegasus	2021	10	14	14
20	Etkili İnsanların 7 Alışkanlığı	Stephen Covey	Varlık	2016	10	10	10
21	Saatleri Ayarlama Enstitüsü	Ahmet Hamdi Tanpınar	Dergah	2017	1	9	9
22	Yeraltından Notlar	Fyodor Dostoyevski	İş Bankası	2019	1	7	6
23	Beyaz Diş	Jack London	İthaki	2018	1	11	11
24	Zamanın Kısa Tarihi	Stephen Hawking	Alfa	2016	2	8	8
25	Kozmos	Carl Sagan	Altın Kitaplar	2019	2	10	10
26	Bilimin Serüveni	James Trefil	TÜBİTAK	2015	2	6	6
27	Tarihin İzinde	İlber Ortaylı	Kronik	2020	3	12	12
28	Avrupa Tarihi	Norman Davies	İnkılap	2018	3	7	7
29	Cumhuriyetin İlk Yılları	Feroz Ahmad	İletişim	2017	3	5	5
30	Computer Networking	James Kurose	Pearson	2021	4	6	6
31	The Linux Command Line	William Shotts	No Starch Press	2020	4	8	8
32	Python Crash Course	Eric Matthes	No Starch Press	2019	4	10	10
33	Database System Concepts	Silberschatz	McGraw-Hill	2018	4	5	4
34	Sokratesin Savunması	Platon	İş Bankası	2016	5	6	6
35	Ahlakın Soykütüğü	Friedrich Nietzsche	Say	2017	5	4	3
36	Mutluluk Üzerine	Seneca	Kabalcı	2018	5	7	7
37	Psikolojinin Temelleri	David Myers	Palme	2019	6	6	6
38	Bilinçaltının Gücü	Joseph Murphy	Koridor	2018	6	9	9
39	Davranış Bilimi	Dan Ariely	Optimist	2020	6	8	8
40	Edebiyat Dersleri	Vladimir Nabokov	İletişim	2016	7	5	5
41	Şiirler	Cemal Süreya	YKY	2017	7	10	9
42	Modern Türk Hikayesi	Mehmet Kaplan	Dergah	2015	7	6	6
43	Öğretim İlke ve Yöntemleri	Sönmez	Anı	2019	8	7	7
44	Sınıf Yönetimi	Zeki Kaya	Pegem	2018	8	6	6
45	Eğitimde Ölçme	Halil Tekin	Yargı	2017	8	5	4
46	Engineering Mathematics	Erwin Kreyszig	Wiley	2018	9	6	6
47	Control Systems	Norman Nise	Wiley	2019	9	5	5
48	Microelectronics	Sedra & Smith	Oxford	2017	9	4	4
49	Düşün ve Zengin Ol	Napoleon Hill	Olympia	2016	10	11	11
50	Odaklanma	Cal Newport	Metropolis	2019	10	9	9
51	Mindset	Carol Dweck	Sola Unitas	2020	10	8	8
83	1984	George Orwell	Can Yayınları	2021	1	15	14
84	Hayvan Çiftliği	George Orwell	Can Yayınları	2020	1	20	18
85	Burma Günleri	George Orwell	İletişim	2019	1	8	5
86	Aspidistra	George Orwell	İletişim	2018	1	6	0
\.

