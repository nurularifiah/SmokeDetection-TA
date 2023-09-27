# setting navigasi dashboard
Navigation = [
    
    {
        'nav_header' : 'CCTV',
        'nav_data' : [
            {
                'type' : 'collapse',
                'nama' : 'Management CCTV',
                'id' : 'broadcast',
                'link' : 'Dashboard.index',
                'icon' : 'menu-icon mdi mdi-camera-enhance',
                'sub_nav' : [
                    {
                        'nama' : 'AI Detection',
                        'link' : 'Dashboard.cctv.daftarCCTV'
                    },
                    {
                        'nama' : 'Tabel Report Deteksi',
                        'link' : 'Dashboard.cctv.dataMaster'
                    },
                ]
            },
        ]
    },
    {
        'nav_header' : 'Umum',
        'nav_data' : [
            {
                'type' : 'non-collapse',
                'nama' : 'Keterangan',
                'link' : 'Dashboard.report.Datareport',
                'icon' : 'menu-icon mdi mdi-account-card-details',
            },
        ]
    },
]