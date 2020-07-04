import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np
import dash_table
import json #Read data to

#-----------------------------for Zooming------------------------------------------
country_bounding_boxes = {
    'AFG': ('Afghanistan', 60.5284298033, 29.318572496, 75.1580277851, 38.4862816432),
    'ALB': ('Albania',19.26319695, 39.65032959, 21.04966545, 42.6607132),
    'DZV': ('Algeria',-8.67386818, 18.96003151, 11.98891068, 37.09513855),
    'ASM': ('American Samoa',-171.090271, -14.54888916, -168.14305115, -11.04777813),
    'AND': ('Andorra',1.41371596, 42.42884445, 1.78420889, 42.65231705),
    'AGO': ('Angola', 11.6400960629, -17.9306364885, 24.0799052263, -4.43802336998),
    'AIA': ('Anguilla',-63.4295845031738, 18.1543064117432, -62.9240264892577, 18.5954170227051),
    'ATG': ('Antigua and Barbuda',-62.34902954, 16.93152809, -61.65652847, 17.72958374),
    'ARG': ('Argentina', -73.4154357571, -55.25, -53.628348965, -21.8323104794),
    'ARM': ('Armenia', 43.5827458026, 38.7412014837, 46.5057198423, 41.2481285671),
    'ABW': ('Aruba',-70.0634689331055, 12.4123611450195, -69.8654174804687, 12.6240291595459),
    'AUS': ('Australia', 113.338953078, -43.6345972634, 153.569469029, -10.6681857235),
    'AUT': ('Austria', 9.47996951665, 46.4318173285, 16.9796667823, 49.0390742051),
    'AZE': ('Azerbaijan', 44.7939896991, 38.2703775091, 50.3928210793, 41.8606751572),
    'BHS': ('Bahamas', -78.98, 23.71, -77.0, 27.04),
    'BHR': ('Bahrain',50.27466965, 25.55624962, 50.82485962, 26.2887516),
    'BGD': ('Bangladesh', 88.0844222351, 20.670883287, 92.6727209818, 26.4465255803),
    'BRB': ('Barbados',-59.6506958, 13.04458427, -59.41930389, 13.33514023),
    'BLR': ('Belarus',23.1783371, 51.2695694, 32.79460907, 56.16836166),
    'BEL': ('Belgium', 2.51357303225, 49.5294835476, 6.15665815596, 51.4750237087),
    'BLZ': ('Belize',-89.2241745, 15.89265823, -87.48596954, 18.49728966),
    'BEN': ('Benin', 0.772335646171, 6.14215770103, 3.79711225751, 12.2356358912),
    'BMU': ('Bermuda',-64.88777924, 32.24666595, -64.64620209, 32.47722626),
    'BTN': ('Bhutan', 88.8142484883, 26.7194029811, 92.1037117859, 28.2964385035),
    'BOL': ('Bolivia', -69.5904237535, -22.8729187965, -57.4983711412, -9.76198780685),
    'BES': ('Bonaire, Sint Eustatius and Saba',-68.42069244, 12.0243063, -62.94180679, 17.65069389),
    'BIH': ('Bosnia and Herzegovina', 15.7500260759, 42.65, 19.59976, 45.2337767604),
    'BWA': ('Botswana', 19.8954577979, -26.8285429827, 29.4321883481, -17.6618156877),
    'BRA': ('Brazil', -73.9872354804, -33.7683777809, -34.7299934555, 5.24448639569),
    'VGB': ('British Virgin Islands',-64.8501358, 18.30597305, -64.27041626, 18.7495842),
    'BRN': ('Brunei Darussalam', 114.204016555, 4.007636827, 115.450710484, 5.44772980389),
    'BGR': ('Bulgaria', 22.3805257504, 41.2344859889, 28.5580814959, 44.2349230007),
    'BFA': ('Burkina Faso', -5.47056494793, 9.61083486576, 2.17710778159, 15.1161577418),
    'BDI': ('Burundi', 29.0249263852, -4.49998341229, 30.752262811, -2.34848683025),
    'CPV': ('Cabo Verde',-25.36180305, 14.80180454, -22.65680504, 17.20541573),
    'KHM': ('Cambodia', 102.3480994, 10.4865436874, 107.614547968, 14.5705838078),
    'CMR': ('Cameroon', 8.48881554529, 1.72767263428, 16.0128524106, 12.8593962671),
    'CAN': ('Canada', -140.99778, 41.6751050889, -52.6480987209, 83.23324),
    'CYM': ('Cayman Islands',-81.4201355, 19.26263809, -79.72264099, 19.75736046),
    'CAF': ('Central African Republic', 14.4594071794, 2.2676396753, 27.3742261085, 11.1423951278),
    'TCD': ('Chad', 13.5403935076, 7.42192454674, 23.88689, 23.40972),
    '0':   ('Channel Islands', 0,0,0,0 ), #MISSING 
    'CHL': ('Chile', -75.6443953112, -55.61183, -66.95992, -17.5800118954),
    'CHN': ('China', 73.6753792663, 18.197700914, 135.026311477, 53.4588044297),
    'HKG': ('Hong Kong',113.8345871, 22.15319443, 114.44097137, 22.56209373),
    'MAC': ('Macau', 113.52875519, 22.10902977, 113.59874725, 22.2173214),
    'TWN': ('Taiwan',120.106188593, 21.9705713974, 121.951243931, 25.2954588893),
    'COL': ('Colombia', -78.9909352282, -4.29818694419, -66.8763258531, 12.4373031682),
    'COM': ('Comoros',43.22874832, -12.42263985, 44.54097366, -11.36486053),
    'COG': ('Congo', 11.0937728207, -5.03798674888, 18.4530652198, 3.72819651938),
    'COK': ('Cook Islands',-165.879440307617, -21.9590873718262, -157.320556640625, -8.91497898101801),
    'CRI': ('Costa Rica', -85.94172543, 8.22502798099, -82.5461962552, 11.2171192489),
    'HRV': ('Croatia', 13.6569755388, 42.47999136, 19.3904757016, 46.5037509222),
    'CUB': ('Cuba', -84.9749110583, 19.8554808619, -74.1780248685, 23.1886107447),
    'CUW': ('Curaçao',-69.1626358032227, 11.9781951904298, -68.6393051147461, 12.3929176330567),
    'CYP': ('Cyprus', 32.2566671079, 34.5718694118, 34.0048808123, 35.1731247015),
    'CZE': ('Czechia', 12.2401111182, 48.5553052842, 18.8531441586, 51.1172677679),
    'CIV': ('Côte d\'Ivoire',-8.59930229, 4.36180687, -2.49489689, 10.73663998),
    'PRK': ('Democratic People\'s Republic of Korea', 124.265624628, 37.669070543, 130.780007359, 42.9853868678),
    'COD': ('Democratic Republic of the Congo', 12.1823368669, -13.2572266578, 31.1741492042, 5.25608775474),
    'DNK': ('Denmark', 8.08997684086, 54.8000145534, 12.6900061378, 57.730016588),
    'DJI': ('Djibouti', 41.66176, 10.9268785669, 43.3178524107, 12.6996385767),
    'DMA': ('Dominica' ,-61.48014069, 15.20625114, -61.24013901, 15.64013863),
    'DMA': ('Dominican Republic', -71.9451120673, 17.598564358, -68.3179432848, 19.8849105901),
    'ECU': ('Ecuador', -80.9677654691, -4.95912851321, -75.2337227037, 1.3809237736),
    'EGY': ('Egypt', 24.70007, 22.0, 36.86623, 31.58568),
    'SLV': ('El Salvador', -90.0955545723, 13.1490168319, -87.7235029772, 14.4241327987),
    'GIN': ('Equatorial Guinea', 5.61644125, -1.46763897, 11.33743668, 3.78874993),
    'ERI': ('Eritrea', 36.3231889178, 12.4554157577, 43.0812260272, 17.9983074),
    'EST': ('Estonia', 23.3397953631, 57.4745283067, 28.1316992531, 59.6110903998),
    'SWZ': ('Eswatini', 30.6766085141, -27.2858794085, 32.0716654803, -25.660190525),
    'ETH': ('Ethiopia', 32.95418, 3.42206, 47.78942, 14.95943),
    'FLK': ('Falkland Islands (Malvinas)',-61.460277557373, -52.9193038940429, -57.6868896484374, -50.9959716796875),
    'FRO': ('Faroe Islands', -7.6833334, 61.39374924, -6.2458334, 62.39166641),
    'FJI': ('Fiji', -180.0, -18.28799, 180.0, -16.0208822567),
    'FIN': ('Finland', 20.6455928891, 59.846373196, 31.5160921567, 70.1641930203),
    'FRA': ('France', -5.14375114, 41.33375168, 9.56041622, 51.08939743),
    'GUF': ('French Guiana',-54.54182434, 2.12872291, -51.60593033, 5.75180578),
    'PYF': ('French Polynesia',-154.72729492, -27.90062714, -134.45111084, -7.89492893),
    'DEU': ('Germany', 5.98865807458, 47.3024876979, 15.0169958839, 54.983104153),
    'GAB': ('Gabon', 8.79799563969, -3.97882659263, 14.4254557634, 2.32675751384),
    'GEO': ('Georgia', 39.9550085793, 41.0644446885, 46.6379081561, 43.553104153),
    'GHA': ('Ghana', -3.24437008301, 4.71046214438, 1.0601216976, 11.0983409693),
    'GMB': ('Gambia', -16.8415246241, 13.1302841252, -13.8449633448, 13.8764918075),
    'GIB': ('Gibraltar',-5.36764001846308, 36.1084709167481, -5.33847188949585, 36.1571540832521),
    'GRC': ('Greece', 20.1500159034, 34.9199876979, 26.6041955909, 41.8269046087),
    'GRL': ('Greenland', -73.297, 60.03676, -12.20855, 83.64513),
    'GRD': ('Grenada',-61.80208206, 11.98430538, -61.3781929, 12.54013824),
    'GLP': ('Guadeloupe', -61.8101387, 15.83152676, -61.00013733, 16.51486206),
    'GUM': ('Guam',144.61791992, 13.23426056, 144.9569397, 13.65432358),
    'GTM': ('Guatemala', -92.2292486234, 13.7353376327, -88.2250227526, 17.8193260767),
    'GNB': ('Guinea-Bissau', -16.6774519516, 11.0404116887, -13.7004760401, 12.6281700708),
    'GUY': ('Guyana', -61.4103029039, 1.26808828369, -56.5393857489, 8.36703481692),
    'HTI': ('Haiti', -74.4580336168, 18.0309927434, -71.6248732164, 19.9156839055),
    '0':   ('Holy See',0 ,0 ,0 ,0 ),#MISSING
    'HND': ('Honduras', -89.3533259753, 12.9846857772, -83.147219001, 16.0054057886), 
    'HUN': ('Hungary', 16.2022982113, 45.7594811061, 22.710531447, 48.6238540716),
    'IRL': ('Ireland', -9.97708574059, 51.6693012559, -6.03298539878, 55.1316222195),
    'IND': ('India', 68.1766451354, 7.96553477623, 97.4025614766, 35.4940095078),
    'IDN': ('Indonesia', 95.2930261576, -10.3599874813, 141.03385176, 5.47982086834),  
    'IRN': ('Iran', 44.1092252948, 25.0782370061, 63.3166317076, 39.7130026312),
    'IRQ': ('Iraq', 38.7923405291, 29.0990251735, 48.5679712258, 37.3852635768),
    'ISL': ('Iceland', -24.3261840479, 63.4963829617, -13.609732225, 66.5267923041),
    'IMN': ('Isle of Man',-4.84118652, 54.03649902, -4.3063879, 54.41819382),
    'ISR': ('Israel', 34.2654333839, 29.5013261988, 35.8363969256, 33.2774264593),
    'ITA': ('Italy', 6.7499552751, 36.619987291, 18.4802470232, 47.1153931748),
    'JAM': ('Jamaica', -78.3377192858, 17.7011162379, -76.1996585761, 18.5242184514),    
    'JOR': ('Jordan', 34.9226025734, 29.1974946152, 39.1954683774, 33.3786864284),
    'JPN': ('Japan', 129.408463169, 31.0295791692, 145.543137242, 45.5514834662),
    'KAZ': ('Kazakhstan', 46.4664457538, 40.6623245306, 87.3599703308, 55.3852501491),
    'KEN': ('Kenya', 33.8935689697, -4.67677, 41.8550830926, 5.506),
    'KIR': ('Kiribati',-174.543395996094, -17.8521137237549, 176.848693847656, 4.69949197769165),
    'KWT': ('Kuwait', 46.5687134133, 28.5260627304, 48.4160941913, 30.0590699326),
    'KGZ': ('Kyrgyzstan', 69.464886916, 39.2794632025, 80.2599902689, 43.2983393418),
    'LAO': ('Laos', 100.115987583, 13.88109101, 107.564525181, 22.4647531194),
    'LVA': ('Latvia', 21.0558004086, 55.61510692, 28.1767094256, 57.9701569688),
    'LBN': ('Lebanon', 35.1260526873, 33.0890400254, 36.6117501157, 34.6449140488),
    'LS':  ('Lesotho', 26.9992619158, -30.6451058896, 29.3251664568, -28.6475017229),
    'LBR': ('Liberia', -11.4387794662, 4.35575511313, -7.53971513511, 8.54105520267),
    'LBY': ('Libya', 9.31941084152, 19.58047, 25.16482, 33.1369957545),
    'LIE': ('Liechtenstein',9.47248077, 47.04738235, 9.63749409, 47.27172852),
    'LTU': ('Lithuania', 21.0558004086, 53.9057022162, 26.5882792498, 56.3725283881),
    'LUX': ('Luxembourg', 5.67405195478, 49.4426671413, 6.24275109216, 50.1280516628), 
    'MAR': ('Morocco', -17.0204284327, 21.4207341578, -1.12455115397, 35.7599881048),
    'MDA': ('Republic of Moldova', 26.6193367856, 45.4882831895, 30.0246586443, 48.4671194525),
    'MDG': ('Madagascar', 43.2541870461, -25.6014344215, 50.4765368996, -12.0405567359),
    'MWI': ('Malawi', 32.6881653175, -16.8012997372, 35.7719047381, -9.23059905359),
    'MYS': ('Malaysia', 100.085756871, 0.773131415201, 119.181903925, 6.92805288332),
    'MDV': ('Maldives',72.6381912231446, -0.70319402217865, 73.7604141235352, 7.10652923583984),
    'MLI': ('Mali', -12.1707502914, 10.0963607854, 4.27020999514, 24.9745740829),
    'MLT': ('Malta',14.18359756, 35.7859726, 14.57652664, 36.08235931),
    'MHL': ('Marshall Islands',160.795272827148, 4.57250118255627, 172.172607421875, 14.7231884002687),
    'MTQ': ('Martinique',-61.22902679, 14.38819408, -60.80875015, 14.87902832),
    'MRT': ('Mauritania', -17.0634232243, 14.6168342147, -4.92333736817, 27.3957441269),
    'MUS': ('Mauritius',56.58569336, -20.52569389, 63.50347137, -10.33708191),
    'MYT': ('Mayotte',45.01791763, -13.00625134, 45.30014038, -12.63569546),
    'MEX': ('Mexico', -117.12776, 14.5388286402, -86.811982388, 32.72083),
    'FSM': ('Micronesia',137.42527771, 1.02527702, 163.03555298, 10.09062386),
    'MCO': ('Monaco',7.40952730178844, 43.7226371765137, 7.44013786315924, 43.750888824463),
    'MNG': ('Mongolia', 87.7512642761, 41.5974095729, 119.772823928, 52.0473660345),
    'MNE': ('Montenegro', 18.45892334, 41.84791565, 20.31764793, 43.56264114),
    'MSR': ('Montserrat',-62.24180603, 16.67486191, -62.14458466, 16.82430649),
    'MOZ': ('Mozambique', 30.1794812355, -26.7421916643, 40.7754752948, -10.3170960425),
    'MMR': ('Myanmar', 92.3032344909, 9.93295990645, 101.180005324, 28.335945136),
    'NAM': ('Namibia', 11.7341988461, -29.045461928, 25.0844433937, -16.9413428687),
    'NRU': ('Nauru',166.90953064, -0.55431199, 166.95933533, -0.502065),
    'NPL': ('Nepal', 80.0884245137, 26.3978980576, 88.1748043151, 30.4227169866),
    'NLD': ('Netherlands', 3.31497114423, 50.803721015, 7.09205325687, 53.5104033474),
    'NCL': ('New Caledonia', 164.029605748, -22.3999760881, 167.120011428, -20.1056458473),
    'NZL': ('New Zealand', 166.509144322, -46.641235447, 178.517093541, -34.4506617165),
    'NER': ('Niger', 0.295646396495, 11.6601671412, 15.9032466977, 23.4716684026),
    'NGA': ('Nigeria', 2.69170169436, 4.24059418377, 14.5771777686, 13.8659239771),
    'NIC': ('Nicaragua', -87.6684934151, 10.7268390975, -83.147219001, 15.0162671981),
    'NIU': ('Niue',-169.950836181641, -19.156156539917, -169.77360534668, -18.9522228240966),
    'MKD': ('North Macedonia', 20.46315, 40.8427269557, 22.9523771502, 42.3202595078),
    'MNP': ('Northern Mariana Islands', 144.88499451, 14.10999966, 146.06604004, 20.5549984),
    'NOR': ('Norway', 4.99207807783, 58.0788841824, 31.29341841, 80.6571442736),
    'OMN': ('Oman', 52.0000098, 16.6510511337, 59.8080603372, 26.3959343531),
    'PAK': ('Pakistan', 60.8742484882, 23.6919650335, 77.8374507995, 37.1330309108),
    'PAN': ('Panama', -82.9657830472, 7.2205414901, -77.2425664944, 9.61161001224),
    'PRY': ('Paraguay', -62.6850571357, -27.5484990374, -54.2929595608, -19.3427466773),
    'PER': ('Peru', -81.4109425524, -18.3479753557, -68.6650797187, -0.0572054988649),
    'PHL': ('Philippines',117.17427453, 5.58100332277, 126.537423944, 18.5052273625),
    'PLW': ('Palau',131.11985779, 2.97138309, 134.72138977, 8.09416676),
    'GIN': ('Papua New Guinea',140.84049988, -11.65538025, 157.03778076, -0.75583303),
    'POL': ('Poland', 14.0745211117, 49.0273953314, 24.0299857927, 54.8515359564),
    'PRI': ('Puerto Rico', -67.2424275377, 17.946553453, -65.5910037909, 18.5206011011),
    'PRT': ('Portugal', -9.52657060387, 36.838268541, -6.3890876937, 42.280468655),
    'QAR': ('Qatar', 50.7439107603, 24.5563308782, 51.6067004738, 26.1145820175),
    'KOR': ('Republic of Korea', 126.117397903, 34.3900458847, 129.468304478, 38.6122429469),#SOUTH KOREA 
    'ROU': ('Romania', 20.2201924985, 43.6884447292, 29.62654341, 48.2208812526),
    'RUS': ('Russian Federation', -180.0, 41.151416124, 180.0, 81.2504),
    'RWA': ('Rwanda', 29.0249263852, -2.91785776125, 30.8161348813, -1.13465911215),
    'REU': ('Réunion',0 ,0 , 0, 0),#MISSING
    'BLM': ('Saint Barthélemy', 0,0 ,0 ,0 ),#MISSING
    'SHN': ('Saint Helena',-14.42111206, -40.37138748, -5.63145208, -7.88916779),
    'KNA': ('Saint Kitts and Nevis',-62.8643074, 17.09347153, -62.53930664, 17.41819382),
    'LCA': ('Saint Lucia',-61.08013916, 13.70708275, -60.8698616, 14.11041737),
    'MAF': ('Saint Martin (French part)',-63.153751373291, 18.0453529357911, -62.9695816040038, 18.1259727478027),
    'SPM': ('Saint Pierre and Miquelon',-56.40611267, 46.74888992, -56.12643814, 47.14500046),
    'VCT': ('Saint Vincent and the Grenadines', -61.46097183, 12.5787487, -61.11402893, 13.3834734),
    'WSM': ('Samoa',-172.80412292, -14.07722092, -171.39770508, -13.43980885),
    'SMR': ('San Marino',12.40066433, 43.89465332, 12.51412296, 43.99569321),
    'STP': ('Sao Tome and Principe',6.45986223, -0.014027, 7.4626379, 1.70152903),
    'SAU': ('Saudi Arabia', 34.6323360532, 16.3478913436, 55.6666593769, 32.161008816),
    'SEN': ('Senegal', -17.6250426905, 12.332089952, -11.4678991358, 16.5982636581),
    'SRB': ('Serbia', 18.82982, 42.2452243971, 22.9860185076, 46.1717298447),
    'SYC': ('Seychelles', 46.20367813, -10.22735977, 56.29568481, -3.7126379),
    'SLE': ('Sierra Leone', -13.2465502588, 6.78591685631, -10.2300935531, 10.0469839543),
    'SGP': ('Singapore', 103.60905457, 1.16638994, 104.08580017, 1.47138798),
    'SXM': ('Sint Maarten (Dutch part)',-63.1394309997558, 17.9998607635499, -62.9998626708984, 18.063549041748),
    'SVK': ('Slovakia', 16.8799829444, 47.7584288601, 22.5581376482, 49.5715740017),
    'SVN': ('Slovenia',13.6981099789, 45.4523163926, 16.5648083839, 46.8523859727),
    'SLB': ('Solomon Islands',155.39250183, -12.30833435, 170.19250488, -4.44521999),
    'SOM': ('Somalia', 40.98105, -1.68325, 51.13387, 12.02464),
    'ZAF': ('South Africa', 16.3449768409, -34.8191663551, 32.830120477, -22.0913127581),
    'SDN': ('Sudan', 21.93681, 8.61972971293, 38.4100899595, 22.0),
    'SSD': ('South Sudan', 23.8869795809, 3.50917, 35.2980071182, 12.2480077571),
    'ESP': ('Spain', -9.39288367353, 35.946850084, 3.03948408368, 43.7483377142),
    'LKA': ('Sri Lanka', 79.6951668639, 5.96836985923, 81.7879590189, 9.82407766361),
    'PSE': ('Palestine', 34.22902679, 31.22360611, 35.57545471, 32.55156708),
    'SUR': ('Suriname', -58.0446943834, 1.81766714112, -53.9580446031, 6.0252914494),
    'SWE': ('Sweden', 11.0273686052, 55.3617373725, 23.9033785336, 69.1062472602),
    'CHE': ('Switzerland', 6.02260949059, 45.7769477403, 10.4427014502, 47.8308275417),
    'SYR': ('Syrian Arab Republic', 35.7007979673, 32.312937527, 42.3495910988, 37.2298725449),
    'TJK': ('Tajikistan', 67.4422196796, 36.7381712916, 74.9800024759, 40.9602133245),
    'THA': ('Thailand', 97.3758964376, 5.69138418215, 105.589038527, 20.4178496363),
    'TLS': ('Timor-Leste', 124.04465485, -9.50465298, 127.34249878, -8.12694454),
    'TGO': ('Togo', -0.0497847151599, 5.92883738853, 1.86524051271, 11.0186817489),
    'TKL': ('Tokelau',-172.52082825, -9.44399643, -171.18139648, -8.53194332),
    'TON': ('Tonga', -176.21383667, -22.34972382, -173.73500061, -15.5657959),
    'TTO': ('Trinidad and Tobago',-61.93013763, 10.04291725, -60.4920845, 11.35958481),
    'TUN': ('Tunisia', 7.52448164229, 30.3075560572, 11.4887874691, 37.3499944118),
    'TUR': ('Turkey', 26.0433512713, 35.8215347357, 44.7939896991, 42.1414848903),
    'TKM': ('Turkmenistan', 52.5024597512, 35.2706639674, 66.5461503437, 42.7515510117),
    'TCA': ('Turks and Caicos Islands',-72.48319244, 21.17708588, -71.08208466, 21.96263885),
    'TUV': ('Tuvalu',176.05874634, -10.79187012, 179.87135315, -5.64249992),
    'UGA': ('Uganda', 29.5794661801, -1.44332244223, 35.03599, 4.24988494736),
    'UKR': ('Ukraine', 22.0856083513, 44.3614785833, 40.0807890155, 52.3350745713),
    'ARE': ('United Arab Emirates', 51.5795186705, 22.4969475367, 56.3968473651, 26.055464179),
    'GBR': ('United Kingdom', -7.57216793459, 49.959999905, 1.68153079591, 58.6350001085),
    'TZA': ('United Republic of Tanzania', 29.3399975929, -11.7209380022, 40.31659, -0.95),
    'VIR': ('United States Virgin Islands', -65.08652496, 17.67291641, -64.56485748, 18.41569519),
    'USA': ('United States of America',-179.15055847, 18.9098587, 179.77340698, 72.6875),
    'URY': ('Uruguay', -58.4270741441, -34.9526465797, -53.209588996, -30.1096863746),
    'UZB': ('Uzbekistan', 55.9289172707, 37.1449940049, 73.055417108, 45.5868043076),
    'VE':  ('Venezuela', -73.3049515449, 0.724452215982, -59.7582848782, 12.1623070337),
    'VNM': ('Viet Nam', 102.170435826, 8.59975962975, 109.33526981, 23.3520633001), #---Vietnam
    'VUT': ('Vanuatu', 166.629136998, -16.5978496233, 167.844876744, -14.6264970842),
    'WLF': ('Wallis and Futuna Islands', 0,0 ,0 ,0 ),#MISSING
    'ESH': ('Western Sahara',-17.10541534, 20.76958275, -8.67001343, 27.68309784),
    'YEM': ('Yemen', 42.6048726743, 12.5859504257, 53.1085726255, 19.0000033635),
    'ZMB': ('Zambia', 21.887842645, -17.9612289364, 33.4856876971, -8.23825652429),
    'ZWE': ('Zimbabwe', 25.2642257016, -22.2716118303, 32.8498608742, -15.5077869605)  
##    'AQ': ('Antarctica', -180.0, -90.0, 180.0, -63.2706604895),
##    'TF': ('Fr. S. and Antarctic Lands', 68.72, -49.775, 70.56, -48.625),
##    'CI': ('Ivory Coast', -8.60288021487, 4.33828847902, -2.56218950033, 10.5240607772),
##    'DZ': ('Algeria', -8.68439978681, 19.0573642034, 11.9995056495, 37.1183806422),
##    'GQ': ('Eq. Guinea', 9.3056132341, 1.01011953369, 11.285078973, 2.28386607504),
##    'ME': ('Montenegro', 18.45, 41.87755, 20.3398, 43.52384),
##    'PG': ('Papua New Guinea', 141.000210403, -10.6524760881, 156.019965448, -2.50000212973),
##    'SB': ('Solomon Is.', 156.491357864, -10.8263672828, 162.398645868, -6.599338474150),
##    'TL': ('East Timor', 124.968682489, -9.39317310958, 127.335928176, -8.27334482181),
##    'TT': ('Trinidad and Tobago', -61.95, 10.0, -60.895, 10.89),
##    'PS': ('West Bank', 34.9274084816, 31.3534353704, 35.5456653175, 32.5325106878),

}

bounds=pd.DataFrame.from_dict(country_bounding_boxes)
bounds=bounds.T
bounds=bounds.reset_index()
bounds=bounds.drop(['index'],axis=1)
print(bounds)

app_colors = {
    'background': '#0C0F0A',
    'text': '#FFFFFF',
    'sentiment-plot':'#41EAD4',
    'volume-bar':'#FBFC74',
    'someothercolor':'#FF206E',
}
files = ['Popuation_forecasted_Cleaned_J_L.xlsx', 'GDPForecast_Cleaned_J_L.xlsx', 'Popuation_forecasted_Cleaned2_J_L.xlsx']
rawData = pd.read_excel(files[1])
PlotData=rawData
print(PlotData)
PlotData=PlotData.set_index("Country")
PlotData=PlotData.T
PlotData=PlotData.drop(['Country Code'])
print(PlotData)

##fileName1='GDPForecast_Cleaned-J, L.xlsx'
##fileName2='Popuation_forecasted_Cleaned- J, L.xlsx'

xx = pd.read_excel(files[0])

countries_list = xx ['Country'].tolist()
countries_list.insert(0,"Select Desired Country:")
countries_list=pd.DataFrame.from_dict(countries_list)
new_head= countries_list.iloc[0] 
countries_list = countries_list[1:]
countries_list.columns = new_head 
countries_list=countries_list.sort_values(by=["Select Desired Country:"])


years=xx.columns.tolist()

year1=int(years[2])
yearN=int(years[-1])
A=[str(i) for i in years]
xx.columns=A
slidY = {}
k=0
for i in years:
    if (k%5==0):
        slidY[i] = str(i)
        k=k+1
    else:
        k=k+1
        continue

print(xx)




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__,external_stylesheets = external_stylesheets )
app.layout = html.Div([
    html.Div([
        
    html.Div(className='row', children=[html.Br(),
                                        html.Br(),
                                        html.H1('Welcome to the page for Visualization of the Global Energy data Base',
                                                style={'color':"#CECECE",'font-size':34,'font-family': 'fantasy','margin-top': 30}),
                                        html.Img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/TU_Muenchen_Logo.svg/1200px-TU_Muenchen_Logo.svg.png",
                                                style={'height': '20%',
                                                        'width': '20%',
                                                        'float': 'right',
                                                        'position': 'relative',
                                                        'margin-top': -80,
                                                        'margin-right': 40}
                                                 )
                                        ],
             style={'width':'98%','margin-left':30,'margin-right':10,'max-width':50000}),
    html.Br(),

    html.Div([
        html.Div(className='three columns',style={'height':'1826px','backgroundColor': '#262626'},
                 children=[
                           html.H3('Top 10 Countries ', style={'font-family': 'fantasy','font-size':40,'color': '#fa2007',}),
                           html.Div(id='top-countries-output-year', style={'font-size': 60, 'font-family':'fantasy', 'color': '#fffc4a',"text-align": "center"}),
                           html.Div(dcc.Graph(id='Top-Countries'),style={'width': '100%','margin-left': 20})]),


        html.Div(className='three columns',children=[html.Div(id='output_data'),
                                                    html.Label(['Choose Indicator:'],style={'font-weight': 'bold','font-size':30, "text-align": "left",'color': '#fa2007','font-family':'fantasy'}),
                                                    dcc.Dropdown(id='my_dropdown',options=[{'label': 'Population', 'value': 'population'},
                                                                                           {'label': 'GDP', 'value': 'GDP'},
                                                                                           {'label': 'Primary Energy Consumption', 'value': 'PEC'}],
                                                                 value= 'population',
                                                                 style = {'font-size': 18,'font-family':'Georgia','verticalAlign' : "middle"}),
                                                    html.H3(id='GlobalMap-output-container', style={'font-family': 'fantasy','font-size':30, 'color': '#fa2007'}),
                                                    dcc.Graph(id='GlobalMap'),
                                                    html.Div(id='slider-output-container', style={'font-size': '16', 'font-family': 'Open Sans', 'color': '#baffa8'}),
                                                    html.Br(),
                                                    dcc.Slider(id='year-slider',min=year1,max=yearN,value=year1,marks=slidY,step=1,),
                                                    html.Br(),html.Br(),
                                                    dcc.Graph(id='Chart')],style={'width': '49%','verticalAlign':'middle'}),


        html.Div(className='two columns', children=[html.Br(),
                                                    dash_table.DataTable(
                                                        id='table',
                                                        columns=[{"name":i,"id":i} for i in countries_list.columns[0:]],
                                                        page_current=0,
                                                        page_size=300,
                                                        data=countries_list.to_dict("rows"),
                                                        
                                                        css= [{'selector': 'tr:hover', 'rule': 'background-color:  #80FF80'}],
                                                        style_table={'height':'1000px','overflowY': 'scroll'},
                                                        style_cell={'minWidth': '0px', # min width of col
                                                                    'maxWidth': '100px',# max width of col
                                                                    'overflow-x':'scroll', #if text overflows scroll 
                                                                    #'textOverflow':'collapse', # if overflow,
                                                                    'textAlign': 'left',
                                                                    'font-family': 'Georgia',
                                                                    'color': '#ffffff',
                                                                    'backgroundColor': '#4a4a4a'},
                                                        style_header={'backgroundColor': 'rgb(0, 0, 0)','font-family': 'fantasy','fontWeight': 'bold','color': '#fa2007'},
                                                        fixed_rows={'headers': True},),
                                                    html.Br(),
                                                    html.Div(id='table-output-container'),],style={'width': '225px',
                                                                                                   'float': 'right',
                                                                                                   'margin-right': 40,
                                                                                                   'font-family': 'fantasy',
                                                                                                   "text-align": "center",
                                                                                                   'color': '#fa2007'}),   
                                                    #html.Div(dcc.Graph(id='bap'),style={'width': '100%','float': 'right','margin-right': -50})])
        ])
     ])],style={'backgroundColor': app_colors['background'], 'margin-top':'-30px', 'height':'2000px',})




@app.callback(
    [Output('Top-Countries', 'figure'),
     Output(component_id='top-countries-output-year', component_property='children'),
     Output('GlobalMap', 'figure'),
     Output(component_id='GlobalMap-output-container',component_property='children'),
     Output(component_id='slider-output-container', component_property='children'),
     Output('year-slider', 'max'),
     Output('year-slider', 'min'),
     Output('year-slider', 'marks'),
     Output(component_id='Chart', component_property='figure'),
     Output(component_id='table-output-container',component_property='children'),],
    [Input(component_id='my_dropdown', component_property='value'),
     Input('year-slider', 'value'),
     Input(component_id='table',component_property='active_cell')],
    [State(component_id='table', component_property='data')])




def update_figure(Chosen_Indicator,selected_year,active_cell,data):
    var=Chosen_Indicator
    y=str(selected_year)
    Year_top10=[] # I had to make this variable because years are stored in different formats for in the two files 

    #read data from files and extract 10 top countries

    if var=='population':
        rawData = pd.read_excel(files[0])
        Year_top10=str(selected_year)
        top10=rawData[['Country',Year_top10]].sort_values(by=[Year_top10],ascending=True)[-10:]
        xlabel="Population"
        PlotData=rawData.set_index("Country")
        PlotData=PlotData.T
        PlotData=PlotData.drop(['Country Code'])
        

    if var=='GDP':
        rawData = pd.read_excel(files[1])
        Year_top10=selected_year
        top10=rawData[['Country',Year_top10]].sort_values(by=[Year_top10],ascending=True)[-10:]
        xlabel="GDP"
        PlotData=rawData.set_index("Country")
        PlotData=PlotData.T
        PlotData=PlotData.drop(['Country Code'])

    if var=='PEC':
        rawData = pd.read_excel(files[2])
        Year_top10=str(selected_year)
        top10=rawData[['Country',Year_top10]].sort_values(by=[Year_top10],ascending=True)[-10:]
        xlabel="Primary Energy Consumption"
        PlotData=rawData.set_index("Country")
        PlotData=PlotData.T
        PlotData=PlotData.drop(['Country Code'])


    #plot the 10 top countries for the chosen indicator (dropDown Menue) and year (slider)

    output_year = " In  {}".format(Year_top10)

    top10plot=px.bar(x=top10[Year_top10],y=top10['Country'],orientation='h',height=600)
    top10plot.update_traces(marker_color='#baffa8')
    top10plot.update_layout(xaxis=dict(title=xlabel,showline=True,showgrid=False,titlefont=dict(family='Georgia',size=20,color='#baffa8'),tickfont=dict(family='Georgia',size=14,color='#ffffff')),
                         yaxis=dict(title=None,showline=True,showgrid=False,titlefont=dict(family='Georgia',size=20,color='#baffa8'),tickfont=dict(family='Georgia',size=14,color='#ffffff')),
                         paper_bgcolor='rgba(0,0,0,0)',
                         plot_bgcolor='rgba(0,0,0,0)'
                        
                         )

   # update slider max, min, marks  

    years=rawData.columns.tolist()

    minVal=int(years[2])
    maxVal=int(years[-1])
    A=[str(i) for i in years]
    rawData.columns=A
    slidY = {}
    k=0
    for i in years:
        if (k%5==0):
            slidY[i] = str(i)
            k=k+1
        else:
            k=k+1
            continue



    # Global Map 
    

    if var=='population':
        container = "Global map of world {}".format(var)
        container_2="Showing data for the year: {}. Please move the slider to select the year of interest.".format(y)
        fig = px.choropleth(rawData, locations='Country Code', color=np.log10(rawData[y]),
                               color_continuous_scale='Viridis'
                                   )
        fig.update_geos(lataxis_range=[-70,90])
        fig.update_layout(coloraxis_colorbar=dict(
            title="Population",
            titlefont=dict(family='Georgia',size=14,color='#fffc4a'),
            tickvals=[3,4,5,6,7,8,9],
            ticktext=['1T', '10T', '100T', '1M', '10M', '100M', '1B'],
            tickfont=dict(family='Georgia',size=14,color='#ffffff')))
        
        fig.update_layout(geo=dict(showframe=False,bgcolor= 'rgba(0,0,0,0)'),margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',)
        fig.update_traces(hovertemplate=None)

        
    if var=='GDP':
        container = "Global map of {} in million USD".format(var)
        container_2="Showing data for the year: {}. Please move the slider to select the year of interest.".format(y)
        fig = px.choropleth(rawData, locations='Country Code', color=np.log10(rawData[y]),color_continuous_scale='Viridis')
        fig.update_geos(lataxis_range=[-70,90])
        fig.update_layout(coloraxis_colorbar=dict(
            title="GDP",
            titlefont=dict(family='Georgia',size=14,color='#fffc4a'),
            tickfont=dict(family='Georgia',size=14,color='#ffffff')))
        fig.update_layout(geo=dict(showframe=False,bgcolor= 'rgba(0,0,0,0)'),margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',)
        fig.update_traces(hovertemplate=None)


    #Data Table for Country Selection 

    Country_Selected=[]
    if active_cell != None:
        choice=list(active_cell.values())
        row=choice[0]
        col=choice[1]
        key=choice[2]
        Country_Selected =data[row][key]
        Coordinates = bounds[bounds[0] == str(Country_Selected)]
        Container_table="Country or Region Under Observation: {}".format(Country_Selected)
##        i=vv.index[vv['ADMIN']==Country_Selected]
##        continent=vv['CONTINENT'][i]
##        continent = continent.tolist()[0]
##        continent=continent.lower()
##        #fig.update_geos(scope=continent,visible=True)
##        #--------------------------------------------------Zoom in the selected Country --------------------------------------------------
##        #--------comment the following line to stop zooming feature---------------------------------------
        #fig.update_geos(lataxis_range=[float(Coordinates[2])-10,float(Coordinates[4])+10],
                       #lonaxis_range=[float(Coordinates[1]-10),float(Coordinates[3])+10]),
        
    if active_cell == None:
        #fig.update_geos(fitbounds="locations")
        Container_table="Country or Region Under Observation: {}".format("World")

    # for the selected country, plot variation of the chosed indicator (dropdown Menu) over years 

    d=[]
    for c in PlotData.columns:
        if Country_Selected !=[]:
                c = Country_Selected
                d=PlotData[c]/10**6
        if Country_Selected ==[]:
            c = "Germany"
            d=PlotData[c]/10**6

    figure=[]

    if var=='population':
        figure=px.bar(x=PlotData.index,y=d)
        ylabel="Population in Millions"
        graph_title= "Population in {}".format(c) 
    if var=='GDP':
        figure=px.line(x=PlotData.index,y=d)
        ylabel="GDP in Millions"
        graph_title= "GDP in {}".format(c) 
    if var=='PEC':
        figure=px.bar(x=PlotData.index,y=d)
        graph_title= "Primary Energy Consumption in {}".format(c) 
        ylabel="Primary Energy Consumption in MW"

        
    figure.update_traces(marker_color='#baffa8')
    figure.update_layout(xaxis=dict(title='Year',showline=True,showgrid=False,titlefont=dict(family='Georgia',size=20,color='#baffa8'),tickfont=dict(family='Georgia',size=14,color='#ffffff')),
                         yaxis=dict(title=ylabel,showline=True,showgrid=False,titlefont=dict(family='Georgia',size=20,color='#baffa8'),tickfont=dict(family='Georgia',size=14,color='#ffffff')),
                         title={'text': graph_title,'y':1.0,'x':0.5,'xanchor': 'center','yanchor': 'top'},titlefont=dict(family='fantasy',size=34,color='#baffa8'),
                         paper_bgcolor='rgba(0,0,0,0)',
                         plot_bgcolor='rgba(0,0,0,0)'
                        
                         )

    return top10plot,output_year,fig, container,container_2,maxVal,minVal,slidY,figure,Container_table  

        




##
                         #title=graph_title,titlefont=dict(family='fantasy',size=34,color='#baffa8'),   
##    figure = {
##        'data': dd,
##        'layout': {
##                   'xaxis':dict(title='Year',titlefont=dict(family='Open Sans',size=20,color='#baffa8')),
##                   'yaxis':dict(title=ylabel,showgrid=False,titlefont=dict(family='Open Sans',size=20,color='#baffa8')),
##                   'title':graph_title,'titlefont':dict(family='fantasy',fontWeight= 'bold',size=34,color='#baffa8'),
##                   'paper_bgcolor':'rgba(0,0,0,0)',
##                   'plot_bgcolor':'rgba(0,0,0,0)',
##                   'marker_color':'rgb(158,202,225)', 'marker_line_color':'rgb(8,48,107)'}
##        }
   


##external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js',
##               'https://pythonprogramming.net/static/socialsentiment/googleanalytics.js']
##
##
##
##for js in external_js:
##    app.scripts.append_script({'external_url': js})


if __name__ == '__main__':
    app.run_server(debug=True)
