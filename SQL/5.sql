select CD_Device.GenericCode, CD_Prj_ODR.ProjectId, CD_Prj_ODR.IsTaskDone, CD_TaskSource.EffortTime, CD_TaskSource.RoundCnt, CD_Prj_ODR.ID as 'ODRID'
FROM CD_Prj_ODR
INNER JOIN CD_TaskSource ON CD_Prj_ODR.ID = CD_TaskSource.SourceID
INNER JOIN CD_Device ON CD_Device.ID = CD_Prj_ODR.DeviceId
WHERE CD_TaskSource.TaskFlowID = 51
AND CD_TaskSource.SourceID IN
(
12252,
12247,
6351,
189,
6497,
18646,
18672,
314,
18668,
5306,
6634,
6640,
18673,
18674,
6377,
18657,
6509,
6505,
6383,
6282,
6386,
6380,
6378,
6333,
6443,
6414,
6495,
6347,
6507,
6400,
6499,
6537,
6501,
6569,
18659,
6408,
18642,
18676,
383,
6294,
6447,
6503,
6451,
6506,
6508,
6500,
18654,
6696,
6560,
6625,
18650,
6502,
6394,
37,
6504,
6619,
313,
6396,
6642,
354,
12233,
18644,
6401,
6630,
6124,
12249,
6516,
6489,
6635,
6531,
6526,
6184,
298,
16560,
6474,
6529,
6519,
6517,
6492,
6178,
6521,
18641,
6399,
18675,
6524,
6518,
6515,
6393,
6392,
6473,
6571,
6395,
6549,
6527,
6633,
18651,
6528,
6611,
6614,
18679,
6533,
13914,
6621,
6618,
5302,
18671,
6624,
6599,
5307,
18670,
305,
6641,
6639,
6638,
6468,
6605,
6525,
6637,
6636,
6616,
316,
330,
18648,
6520,
6606,
6530,
6609,
6379,
18733,
18658,
18677,
18661,
190,
6397,
18712,
18714,
18711,
18713,
6488,
6381,
13903,
18643,
6612,
6402,
6398,
6540,
6714,
6712,
6713,
6690,
12237,
12235,
6522,
6608,
6578,
6430,
6454,
6194,
175,
191,
6656,
6643,
6550,
6486,
246,
6487,
6570,
6384,
6653,
6542,
18748,
18749,
18747,
6573,
18735,
6707,
291,
6471,
6472,
6558,
13905,
12230,
6523,
12223,
12225,
6416,
6146,
13908,
18746,
18744,
6470,
18751,
18750,
18745,
18743,
18742,
18741,
18740,
18739,
18737,
16557,
16554,
6363,
13904,
6718,
6648,
6126,
6655,
6364,
6561,
6391,
6557,
18663,
6556,
6551,
6460,
6555,
18678,
6465,
18839,
6685,
12245,
6715,
18941,
6628,
18859,
18753,
18755,
18664,
18752,
6603,
18756,
18783,
18683,
18919,
18698,
18759,
13915,
6562,
18942,
18681,
13902,
18857,
18774,
18948,
18830,
18762,
18943,
18764,
18889,
18807,
18905,
18765,
18719,
18716,
18715,
18718,
18717,
18652,
18841,
18696,
18704,
18823,
18937,
18910,
18778,
18771,
18645,
18879,
18896,
18692,
6541,
18699,
18886,
18687,
18758,
18853,
18877,
18794,
18805,
18802,
18797,
18785,
18831,
18923,
18842,
18710,
18911,
18697,
18703,
18779,
18772,
18940,
18763,
18855,
18730,
18728,
18727,
18729,
18726,
18725,
18723,
18720,
18724,
18721,
18769,
18907,
18768,
18757,
18904,
18722,
18760,
6272,
6273,
18761,
18918,
18913,
18933,
18893,
18912,
18870,
18734,
18786,
18897,
18695,
18848,
18685,
18777,
18938,
18874,
18817,
18849,
18780,
18787,
18827,
18811,
18927,
18667,
18790,
18832,
18928,
18926,
18920,
18705,
18708,
18776,
18798,
18801,
18820,
18814,
18872,
18939,
18822,
18738,
18810,
18836,
18866,
18972,
6493,
18840,
18854,
18791,
18993,
18868,
18844,
18850,
18931,
18932,
18815,
18847,
18864,
19032,
6613,
18804,
18789,
18929,
18701,
18818,
18860,
18899,
18883,
18851,
18816,
6709,
18862,
18924,
18861,
18871,
19062,
18888,
19033
);