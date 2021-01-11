from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sbs.api.message import UserModelViewSet, MessageModelViewSet, UserModelEndMessageViewSet, EmployeModelViewSet, \
    CompanyModelViewSet

from sbs.Views import DashboardViews, AthleteViews, RefereeViews, ClubViews, CoachViews, DirectoryViews, UserViews, \
    CompetitionViews, AdminViews, HelpViews, PageViews, PreRegistration, EPProjectViews, EmployeeViews, PdfView, \
    TechnicalViews, LogViews, NotificationView, CompanyView, ClaimView

app_name = 'sbs'

router = DefaultRouter()
router.register(r'mesaj', MessageModelViewSet, basename='message-api')
router.register(r'kul', UserModelViewSet, basename='user-api')
router.register(r'kulEndMessage', UserModelEndMessageViewSet, basename='user-api-end')
router.register(r'employess', EmployeModelViewSet, basename='employee-api')
router.register(r'company', CompanyModelViewSet, basename='company-api')



urlpatterns = [

    # Dashboard
    url(r'anasayfa/admin/$', DashboardViews.return_admin_dashboard, name='admin'),
    url(r'anasayfa/sehir-sporcu-sayisi/$', DashboardViews.City_athlete_cout, name='sehir-sporcu-sayisi'),
    url(r'anasayfa/sporcu/$', DashboardViews.return_athlete_dashboard, name='sporcu'),
    url(r'anasayfa/hakem/$', DashboardViews.return_referee_dashboard, name='hakem'),
    url(r'anasayfa/antrenor/$', DashboardViews.return_coach_dashboard, name='antrenor'),
    url(r'anasayfa/federasyon/$', DashboardViews.return_directory_dashboard, name='federasyon'),
    url(r'anasayfa/kulup-uyesi/$', DashboardViews.return_club_user_dashboard, name='kulup-uyesi'),

    # Sporcular
    url(r'sporcu/sporcu-ekle/$', AthleteViews.return_add_athlete, name='sporcu-ekle'),
    url(r'sporcu/sporcular/$', AthleteViews.return_athletes, name='sporcular'),

    # pagenation deneme
    url(r'page/$', PageViews.deneme, name='deneme'),
    url(r'sporcularajax/$', PageViews.return_athletesdeneme, name='sporculardeneme'),

    url(r'sporcu/sporcuKusakEkle/(?P<pk>\d+)$', AthleteViews.sporcu_kusak_ekle, name='sporcu-kusak-ekle'),
    url(r'sporcu/sporcuKusakDuzenle/(?P<belt_pk>\d+)/(?P<athlete_pk>\d+)$', AthleteViews.sporcu_kusak_duzenle,
        name='sporcu-kusak-duzenle'),
    url(r'sporcu/sporcuLisansEkle/(?P<pk>\d+)$', AthleteViews.sporcu_lisans_ekle, name='sporcu-lisans-ekle'),
    url(r'sporcu/sporcuLisansDuzenle/(?P<license_pk>\d+)/(?P<athlete_pk>\d+)$', AthleteViews.sporcu_lisans_duzenle,
        name='sporcu-lisans-duzenle'),
    url(r'sporcu/sporcuLisansDuzenleMobil/(?P<count>\d+)$', AthleteViews.sporcu_lisans_duzenle_mobil,
        name='sporcu-lisans-duzenle-mobil'),
    # ilk degeri verebilmek icin yönlendirme amaci ile kullanildi.
    url(r'sporcu/sporcuLisansDuzenleMobil/$', AthleteViews.sporcu_lisans_duzenle_mobil_ilet,
        name='sporcu-lisans-duzenle-mobil-ilet'),

    url(r'sporcu/sporcuLisansDuzenle/onayla/(?P<license_pk>\d+)/(?P<athlete_pk>\d+)$',
        AthleteViews.sporcu_lisans_onayla, name='sporcu-lisans-onayla'),

    url(r'sporcu/sporcuLisansDuzenle/reddet/(?P<license_pk>\d+)/(?P<athlete_pk>\d+)$',
        AthleteViews.sporcu_lisans_reddet, name='sporcu-lisans-reddet'),
    url(r'sporcu/sporcuLisansDuzenle/lisanssil/(?P<pk>\d+)/(?P<athlete_pk>\d+)$', AthleteViews.sporcu_lisans_sil,
        name='sporcu-lisans-sil'),
    url(r'sporcu/sporcuLisansListesi/onayla/(?P<license_pk>\d+)$',
        AthleteViews.sporcu_lisans_listesi_onayla, name='sporcu-lisans-listesi-onayla'),
    url(r'sporcu/sporcuLisansListesi/onaylaMobil/(?P<license_pk>\d+)/(?P<count>\d+)$',
        AthleteViews.sporcu_lisans_listesi_onayla_mobil, name='sporcu-lisans-listesi-onayla-mobil'),
    # lisans listesinin hepsini onaylama
    url(r'sporcu/sporcuLisansListesi/hepsinionayla/$', AthleteViews.sporcu_lisans_listesi_hepsionay,
        name='sporcu-lisans-hepsini-onayla'),
    # lisanslarin hepsini reddetme
    url(r'sporcu/sporcuLisansListesi/hepsiniReddet/$', AthleteViews.sporcu_lisans_listesi_hepsireddet,
        name='sporcu-lisans-hepsini-reddet'),

    # hepsini beklemeye al
    url(r'sporcu/sporcuLisansListesi/hepsinibekle/$', AthleteViews.sporcu_bekle,
        name='sporcu-lisans-hepsini-bekle'),

    url(r'sporcu/sporcuLisansListesi/reddet/(?P<license_pk>\d+)$',
        AthleteViews.sporcu_lisans_listesi_reddet, name='sporcu-lisans-listesi-reddet'),
    url(r'sporcu/sporcuLisansListesiMobil/reddet/(?P<license_pk>\d+)/(?P<count>\d+)$',
        AthleteViews.sporcu_lisans_listesi_reddet_mobil, name='sporcu-lisans-listesi-reddet-mobil'),
    url(r'sporcu/kusak/$', AthleteViews.return_belt, name='kusak'),
    url(r'sporcu/kusak/sil/(?P<pk>\d+)$', AthleteViews.categoryItemDelete,
        name='categoryItem-delete'),
    url(r'sporcu/kusakDuzenle/(?P<pk>\d+)$', AthleteViews.categoryItemUpdate,
        name='categoryItem-duzenle'),
    url(r'sporcu/sporcuKusakDuzenle/onayla/(?P<belt_pk>\d+)/(?P<athlete_pk>\d+)$',
        AthleteViews.sporcu_kusak_onayla, name='sporcu-kusak-onayla'),
    url(r'sporcu/sporcuKusakReddet/(?P<belt_pk>\d+)/(?P<athlete_pk>\d+)$',
        AthleteViews.sporcu_kusak_reddet, name='sporcu-kusak-reddet'),
    url(r'sporcu/sporcuKusakDuzenle/kusaksil/(?P<pk>\d+)/(?P<athlete_pk>\d+)$', AthleteViews.sporcu_kusak_sil,
        name='sporcu-kusak-sil'),

    # kuşaklarin hepsini beklemeye al
    url(r'sporcu/sporcuKusakbekle',
        AthleteViews.sporcu_kusak_bekle, name='sporcu-kusak-bekle'),
    # kuşak listesinin hepsini onayla
    url(r'sporcu/sporcuKusakListesi/hepsinionayla/$',
        AthleteViews.sporcu_kusak_listesi_hepsinionayla, name='sporcu-kusak-listesi-hepsinionayla'),

    # kuşak hepsini reddet
    url(r'sporcu/sporcuKusakDuzenle/reddet/$',
        AthleteViews.sporcu_kusak_hepsinireddet, name='sporcu-kusak-hepsinireddet'),

    # kusak listesi onay
    url(r'sporcu/sporcuKusakListesi/onayla/(?P<belt_pk>\d+)$',
        AthleteViews.sporcu_kusak_listesi_onayla, name='sporcu-kusak-listesi-onayla'),
    # kuşak listesi reddet
    url(r'sporcu/sporcuKusakListesi/reddet/(?P<belt_pk>\d+)$',
        AthleteViews.sporcu_kusak_listesi_reddet, name='sporcu-kusak-listesi-reddet'),

    url(r'sporcu/sporcuDuzenle/(?P<pk>\d+)$', AthleteViews.updateathletes, name='update-athletes'),
    url(r'sporcu/sporcu-kusak-listesi/$', AthleteViews.sporcu_kusak_listesi, name='kusak-listesi'),
    url(r'sporcu/sporcu-lisans-listesi/$', AthleteViews.sporcu_lisans_listesi, name='lisans-listesi'),
    url(r'sporcu/sporcu-profil-guncelle/$', AthleteViews.updateAthleteProfile,
        name='sporcu-profil-guncelle'),

    # Hakemler
    url(r'hakem/hakem-ekle/$', RefereeViews.return_add_referee, name='hakem-ekle'),
    url(r'hakem/hakemler/$', RefereeViews.return_referees, name='hakemler'),
    url(r'hakem/seviye/$', RefereeViews.return_level, name='seviye'),
    url(r'hakem/seviye/sil/(?P<pk>\d+)$', RefereeViews.categoryItemDelete,
        name='categoryItem-delete-seviye'),
    url(r'hakem/seviye/(?P<pk>\d+)$', RefereeViews.categoryItemUpdate,
        name='categoryItem-duzenle-seviye'),
    url(r'hakem/hakemler/sil/(?P<pk>\d+)$', RefereeViews.deleteReferee,
        name='referee-delete'),
    url(r'hakem/hakemDuzenle/(?P<pk>\d+)$', RefereeViews.updateReferee,
        name='hakem-duzenle'),
    url(r'hakem/hakem-profil-guncelle/$', RefereeViews.updateRefereeProfile,
        name='hakem-profil-guncelle'),
    # /kademe
    url(r'hakem/Hakem-kademe-ekle/(?P<pk>\d+)$', RefereeViews.hakem_kademe_ekle, name='hakem-kademe-ekle'),
    url(r'hakem/Kademe-Duzenle/onayla/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.kademe_onay,
        name='kademe-onayla-hakem'),
    url(r'hakem/Kademe-Duzenle/reddet/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.kademe_reddet,
        name='kademe-reddet-hakem'),
    url(r'hakem/Kademe-Duzenle/güncelle/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.kademe_update,
        name='kademe-güncelle-hakem'),
    url(r'hakem/Kademe-Duzenle/sil/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.kademe_delete,
        name='Kademe-sil-hakem'),
    # /vize
    url(r'hakem/hakem-vize-ekle/(?P<pk>\d+)$', RefereeViews.vısa_ekle, name='hakem-vize-ekle'),
    url(r'hakem/Vize-Duzenle/onayla/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.visa_onay,
        name='hakem-vize-onayla'),
    url(r'hakem/Vize-Duzenle/reddet/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.visa_reddet,
        name='hakem-vize-reddet'),
    url(r'hakem/Vize-Duzenle/guncelle/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.vize_update,
        name='hakem-vize-güncelle'),
    url(r'hakem/Vize-Duzenle/sil/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.vize_delete,
        name='hakem-vize-sil'),

    # Kulüpler
    url(r'kulup/basvuru-listesi/$', PreRegistration.return_preRegistration, name='basvuru-listesi'),
    url(r'kulup/basvuru/onayla/(?P<pk>\d+)$', PreRegistration.approve_preRegistration, name='basvuru-onayla'),
    url(r'kulup/basvuru/reddet/(?P<pk>\d+)$', PreRegistration.rejected_preRegistration, name='basvuru-reddet'),
    url(r'sporcu/basvuru-incele/(?P<pk>\d+)$', PreRegistration.update_preRegistration, name='update-basvuru'),

    url(r'kulup/kulup-ekle/$', ClubViews.return_add_club, name='kulup-ekle'),
    url(r'kulup/kulupler/$', ClubViews.return_clubs, name='kulupler'),
    url(r'kulup/kulup-uyesi-ekle/$', ClubViews.return_add_club_person, name='kulup-uyesi-ekle'),
    url(r'kulup/kulup-uyesi-guncelle/(?P<pk>\d+)$', ClubViews.updateClubPersons, name='kulup-uyesi-guncelle'),
    url(r'kulup/kulup-uyeleri/$', ClubViews.return_club_person, name='kulup-uyeleri'),
    url(r'kulup/kulup-uye-rolu/$', ClubViews.return_club_role, name='kulup-uye-rolu'),
    url(r'kulup/kulup-uye-rolu/sil/(?P<pk>\d+)$', ClubViews.deleteClubRole,
        name='ClubRole-delete'),
    url(r'kulup/kulup-uyeleri/sil/(?P<pk>\d+)$', ClubViews.deleteClubUser,
        name='ClubUser-delete'),

    url(r'kulup/kulup-uyeleri/cikar/(?P<pk>\d+)/(?P<club_pk>\d+)/$', ClubViews.deleteClubUserFromClub,
        name='ClubUser-cikar'),
    url(r'kulup/kulup-antrenorleri/cikar/(?P<pk>\d+)/(?P<club_pk>\d+)/$', ClubViews.deleteCoachFromClub,
        name='ClubCoach-cikar'),

    url(r'kulup/kulupRolDuzenle/(?P<pk>\d+)$', ClubViews.updateClubRole,
        name='updateClubRole'),
    url(r'kulup/kulupler/sil/(?P<pk>\d+)$', ClubViews.clubDelete,
        name='delete-club'),
    url(r'kulup/kulupDuzenle/(?P<pk>\d+)$', ClubViews.clubUpdate,
        name='update-club'),
    url(r'kulup/kusak-sinavlari/$', ClubViews.return_belt_exams, name='kusak-sinavlari'),
    url(r'kulup/kusak-sinavi-sporcu-sec/(?P<pk>\d+)$', ClubViews.choose_athlete, name='kusak-sinavi-sporcu-sec'),
    #

    url(r'kulup/kusak-sinavi-ekle/$', ClubViews.add_belt_exam, name='kusak-sinavi-ekle'),
    url(r'kulup/kusak-sinavi-antroner-sec/(?P<pk>\d+)$', ClubViews.choose_coach, name='kusak-sinavi-antroner-sec'),

    url(r'kulup/kusak-sinavi-antroner-sil/(?P<pk>\d+)/(?P<exam_pk>\d+)$', ClubViews.choose_coach_remove,
        name='kulup-sinavi-antroner-sil'),
    url(r'kulup/kusak-sinavi-sporcu-sil/(?P<pk>\d+)/(?P<exam_pk>\d+)$', ClubViews.choose_athlete_remove,
        name='kulup-sinavi-sporcu-sil'),

    url(r'kulup/kusak-sinavi-ekle/(?P<athlete1>\S+?)$', ClubViews.add_belt_exam, name='kusak-sinavi-ekle'),
    url(r'kulup/kusak-sinavi-duzenle/(?P<pk>\d+)$', ClubViews.update_belt_exam, name='kusak-sinavi-duzenle'),
    url(r'kulup/kusak-sinavlari/sil/(?P<pk>\d+)$', ClubViews.delete_belt_exam, name='kusak-sinavi-sil'),
    url(r'kulup/kusak-sinavlari/incele/(?P<pk>\d+)$', ClubViews.detail_belt_exam, name='kusak-sinavi-incele'),
    url(r'kulup/kusak-sinavlari/onayla/(?P<pk>\d+)$', ClubViews.approve_belt_exam, name='kusak-sinavi-onayla'),
    url(r'kulup/kusak-sinavlari/reddet/(?P<pk>\d+)$', ClubViews.denied_belt_exam, name='kusak-sinavi-reddet'),

    url(r'kulup/kulup-uyesi-profil-guncelle/$', ClubViews.updateClubPersonsProfile,
        name='kulup-uyesi-profil-guncelle'),

    url(r'kulup/kulup-uyesi-sec/(?P<pk>\d+)$', ClubViews.choose_sport_club_user,
        name='choose-sport-club-user'),
    url(r'kulup/kusak-listesi-antroner-sil/(?P<pk>\d+)$', ClubViews.choose_sport_club_user,
        name='choose-sport-club-user'),

    # Antrenörler
    url(r'antrenor/antrenor-ekle/$', CoachViews.return_add_coach, name='antrenor-ekle'),
    url(r'antrenor/antrenorler/$', CoachViews.return_coachs, name='antrenorler'),
    url(r'antrenor/kademe/$', CoachViews.return_grade, name='kademe'),
    url(r'antrenor/kademe/sil/(?P<pk>\d+)$', CoachViews.categoryItemDelete,
        name='categoryItem-delete-kademe'),
    url(r'antrenor/kademeDuzenle/(?P<pk>\d+)$', CoachViews.categoryItemUpdate,
        name='categoryItem-duzenle-kademe'),
    url(r'antrenor/antrenorler/sil/(?P<pk>\d+)$', CoachViews.deleteCoach,
        name='delete-coach'),
    url(r'antrenor/antrenorDuzenle/(?P<pk>\d+)$', CoachViews.coachUpdate,
        name='update-coach'),
    url(r'antrenor/antrenorSec/(?P<pk>\d+)$', ClubViews.choose_coach,
        name='choose-coach'),
    url(r'antrenor/antrenor-profil-guncelle/$', CoachViews.updateCoachProfile,
        name='antrenor-profil-guncelle'),
    url(r'antrenor/antrenor-kademe-ekle/(?P<pk>\d+)$', CoachViews.antrenor_kademe_ekle, name='antrenor-kademe-ekle'),
    #     # vize ekle
    url(r'antrenor/antrenor-vize-ekle/(?P<pk>\d+)$', CoachViews.antrenor_vısa_ekle, name='antrenor-vize-ekle'),

    # Kademe onay reddet sil güncelle liste
    url(r'antrenor/vize-Liste-Reddet/(?P<grade_pk>\d+)$', CoachViews.vize_reddet_liste,
        name='vize-list-reddet'),
    url(r'antrenor/vize-Liste-Onayla/(?P<grade_pk>\d+)$', CoachViews.vize_onayla_liste,
        name='vize-list-onay'),
    url(r'antrenor/Vize-Duzenle/sil/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.vize_delete,
        name='vize-sil'),
    url(r'antrenor/Vize-Reddet/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.vize_reddet, name='vize-reddet'),
    url(r'antrenor/Vize-Duzenle/onayla/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.visa_onay, name='vize-onayla'),
    url(r'antrenor/Kademe-Duzenle/onayla/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.kademe_onay,
        name='kademe-onayla'),
    url(r'antrenor/Kademe-Reddet/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.kademe_reddet, name='kademe-reddet'),
    url(r'antrenor/Kademe-Duzenle/güncelle/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.kademe_update,
        name='kademe-güncelle'),
    url(r'antrenor/Vize-Duzenle/guncelle/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.vize_update,
        name='vize-güncelle'),
    url(r'antrenor/Kademe-Duzenle/sil/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.kademe_delete,
        name='Kademe-sil'),
    url(r'antrenor/Kademe-listesi/', CoachViews.kademe_list, name='kademe-listesi'),
    url(r'antrenor/Vize-listesi/', CoachViews.vize_list, name='vize-listesi'),
    url(r'antrenor/kademe-Liste-Onayla/(?P<grade_pk>\d+)$', CoachViews.kademe_onayla,
        name='kademe-list-onay'),
    url(r'antrenor/kademe-Liste-reddet/(?P<grade_pk>\d+)$', CoachViews.kademe_reddet_liste,
        name='kademe-list-reddet'),
    url(r'antrenor/kademe-Liste-reddet-hepsi$', CoachViews.kademe_reddet_hepsi,
        name='kademe-list-reddet-hepsi'),
    url(r'antrenor/kademe-Liste-onay-hepsi$', CoachViews.kademe_onay_hepsi,
        name='kademe-list-onay-hepsi'),
    url(r'antrenor/kademe-Liste-bekle-hepsi$', CoachViews.kademe_bekle_hepsi, name='kademe-list-bekle-hepsi'),

    # visa seminar
    # Antrenör
    url(r'antrenor/visa-Seminar$', CoachViews.return_visaSeminar, name='visa-seminar'),
    url(r'antrenor/visa-Seminar-ekle$', CoachViews.visaSeminar_ekle, name='visa-seminar-ekle'),
    url(r'antrenor/visa-Seminar-duzenle/(?P<pk>\d+)$', CoachViews.visaSeminar_duzenle, name='seminar-duzenle'),
    url(r'antrenor/visa-Seminar-Onayla/(?P<pk>\d+)$', CoachViews.visaSeminar_onayla, name='seminar-onayla'),
    url(r'antrenor/visa-Seminar/Seminer-sil(?P<pk>\d+)$', CoachViews.visaSeminar_sil, name='seminar-sil'),
    url(r'antrenor/visa-Seminar/antroner-sec/(?P<pk>\d+)$', CoachViews.choose_coach, name='vize-semineri-antroner-sec'),
    url(r'antrenor/visa-Seminar/antroner-sil/(?P<pk>\d+)/(?P<competition>\d+)$', CoachViews.visaSeminar_Delete_Coach,
        name='visaSeminar-antrenör-sil'),
    # Hakem
    url(r'hakem/visa-Seminar$', RefereeViews.return_visaSeminar, name='hakem-visa-seminar'),
    url(r'hakem/visa-Seminar-ekle$', RefereeViews.visaSeminar_ekle, name='hakem-visa-seminar-ekle'),
    url(r'hakem/visa-Seminar-duzenle/(?P<pk>\d+)$', RefereeViews.visaSeminar_duzenle, name='hakem-seminar-duzenle'),
    url(r'hakem/visa-Seminar/Seminer-sil(?P<pk>\d+)$', RefereeViews.visaSeminar_sil, name='hakem-seminar-sil'),
    url(r'hakem/visa-Seminar/hakem-sec/(?P<pk>\d+)$', RefereeViews.choose_referee, name='vize-semineri-hakem-sec'),
    url(r'hakem/visa-Seminar/hakem-sil/(?P<pk>\d+)/(?P<competition>\d+)$', RefereeViews.visaSeminar_Delete_Referee,
        name='visaSeminar-hakem-sil'),
    url(r'hakem/visa-Seminar-Onayla/(?P<pk>\d+)$', RefereeViews.visaSeminar_onayla, name='hakem-seminar-onayla'),

    url(r'hakem/Kademe-listesi/', RefereeViews.kademe_list, name='hakem-kademe-listesi'),
    url(r'hakem/kademe-Liste-Onayla/(?P<referee_pk>\d+)$', RefereeViews.kademe_onayla,
        name='hakem-kademe-list-onay'),
    url(r'hakem/kademe-Liste-reddet/(?P<referee_pk>\d+)$', RefereeViews.kademe_reddet_liste,
        name='hakem-kademe-list-reddet'),
    url(r'hakem/vize-Liste-Reddet/(?P<referee_pk>\d+)$', RefereeViews.vize_reddet_liste,
        name='hakem-vize-list-reddet'),

    url(r'hakem/kademe-Liste-onay-hepsi$', RefereeViews.kademe_onay_hepsi,
        name='hakem-kademe-list-onay-hepsi'),
    url(r'hakem/kademe-Liste-reddet-hepsi$', RefereeViews.kademe_reddet_hepsi,
        name='hakem-kademe-list-reddet-hepsi'),
    url(r'hakem/Vize-listesi/', RefereeViews.vize_list, name='hakem-vize-listesi'),
    url(r'hakem/vize-Liste-Onayla/(?P<referee_pk>\d+)$', RefereeViews.vize_onayla_liste,
        name='hakem-vize-list-onay'),

    # Yönetim Kurulu
    url(r'yonetim/kurul-uyeleri/$', DirectoryViews.return_directory_members, name='kurul-uyeleri'),
    url(r'yonetim/kurul-uyesi-ekle/$', DirectoryViews.add_directory_member, name='kurul-uyesi-ekle'),
    url(r'yonetim/kurul-uyesi-duzenle/(?P<pk>\d+)$', DirectoryViews.update_directory_member,
        name='kurul-uyesi-duzenle'),
    url(r'yonetim/kurul-uyeleri/sil/(?P<pk>\d+)$', DirectoryViews.delete_directory_member,
        name='kurul-uyesi-sil'),
    url(r'yonetim/kurul-uye-rolleri/$', DirectoryViews.return_member_roles, name='kurul-uye-rolleri'),
    url(r'yonetim/kurul-uye-rolleri/sil/(?P<pk>\d+)$', DirectoryViews.delete_member_role,
        name='kurul_uye_rol_sil'),
    url(r'yonetim/kurul-uye-rol-duzenle/(?P<pk>\d+)$', DirectoryViews.update_member_role,
        name='kurul-uye-rol-duzenle'),
    url(r'yonetim/kurullar/$', DirectoryViews.return_commissions, name='kurullar'),
    url(r'yonetim/kurullar/sil/(?P<pk>\d+)$', DirectoryViews.delete_commission,
        name='kurul_sil'),
    url(r'yonetim/kurul-duzenle/(?P<pk>\d+)$', DirectoryViews.update_commission,
        name='kurul-duzenle'),
    url(r'yonetim/yonetim-kurul-profil-guncelle/$', DirectoryViews.updateDirectoryProfile,
        name='yonetim-kurul-profil-guncelle'),

    # Admin
    url(r'admin/admin-profil-guncelle/$', AdminViews.updateProfile,
        name='admin-profil-guncelle'),

    # Kullanıcılar
    url(r'kullanici/kullanicilar/$', UserViews.return_users, name='kullanicilar'),
    url(r'kullanici/kullanicilar/toplu$', UserViews.UserAllMail, name='kullanicilar-toplu-mesaj'),
    url(r'kullanici/kullanici-duzenle/(?P<pk>\d+)$', UserViews.update_user, name='kullanici-duzenle'),
    url(r'kullanici/kullanicilar/aktifet/(?P<pk>\d+)$', UserViews.active_user,
        name='kullanici-aktifet'),
    url(r'kullanici/kullanicilar/kullanici-bilgi-gonder/(?P<pk>\d+)$', UserViews.send_information,
        name='kullanici-bilgi-gonder'),

    # Competition
    url(r'musabaka/musabakalar/$', CompetitionViews.return_competitions, name='musabakalar'),
    url(r'musabaka/musabaka-ekle/$', CompetitionViews.musabaka_ekle, name='musabaka-ekle'),
    url(r'musabaka/musabaka-duzenle/(?P<pk>\d+)$', CompetitionViews.musabaka_duzenle, name='musabaka-duzenle'),
    url(r'musabaka/musabakalar/musabaka-sil(?P<pk>\d+)$', CompetitionViews.musabaka_sil, name='musabaka-sil'),
    url(r'musabaka/musabaka-sporcu-sec/(?P<pk>\d+)$', CompetitionViews.musabaka_sporcu_sec, name='musabaka-sporcu-sec'),
    url(r'musabaka/sporcu-sec/(?P<pk>\d+)/(?P<competition>\d+)$', CompetitionViews.choose_athlete,
        name='catagori-sporcu-sec-ajax'),
    url(r'musabaka/KategorilerinSporculari/$', CompetitionViews.return_sporcu, name='Kategorilerin-Sporculari'),
    url(r'musabaka/musabaka-duzenle/musabaka_sporcu_ekle/(?P<athlete_pk>\d+)/(?P<competition_pk>\d+)$',
        CompetitionViews.musabaka_sporcu_ekle,
        name='musabaka_sporcu_ekle'),
    url(r'musabaka/musabaka-duzenle/kaldir/(?P<pk>\d+)/$', CompetitionViews.musabaka_sporcu_sil,
        name='musabaka-sporcu-kaldir'),
    url(r'musabaka/KategoriEkle/$', CompetitionViews.categori_ekle, name='kategori-ekle'),
    #     Yardım ve destek

    url(r'yardim$', HelpViews.help, name='help'),
    # ETÜT PROJE

    url(r'etut-proje/projeler/$', EPProjectViews.return_projects, name='projeler'),
    url(r'etut-proje/projeler/detay$', EPProjectViews.return_detay, name='detay'),
    url(r'etut-proje/projeler-il/(?P<pk>\d+)$', EPProjectViews.return_projects_city, name='projeler-il'),
    url(r'etut-proje/proje-ekle/$', EPProjectViews.add_project, name='proje-ekle'),
    url(r'etut-proje/proje-duzenle/(?P<pk>\d+)$', EPProjectViews.edit_project, name='proje-duzenle'),
    url(r'etut-proje/proje-duzenle/personel/(?P<pk>\d+)$', EPProjectViews.edit_project_personel, name='proje-incele-personel'),
    url(r'etut-proje/projeler/dokumanekle$', EPProjectViews.dokumanAdd, name='dokumanAdd'),

    url(r'etut-proje/employess/$', EPProjectViews.return_projects_mimar, name='mimarlar'),

    url(r'etut-proje/proje-pdf/(?P<pk>\d+)$', PdfView.edit_project_pdf, name='proje-pdf'),

    url(r'etut-proje/proje-pdf/teknik/(?P<pk>\d+)$', PdfView.edit_project_pdf_teknik, name='proje-pdf-teknik'),
    url(r'etut-proje/proje-pdf/personel/(?P<pk>\d+)$', PdfView.edit_project_pdf_personel, name='proje-pdf-personel'),
    url(r'etut-proje/proje-excel/(?P<pk>\d+)$', PdfView.edit_project_excel, name='proje-excel'),

    url(r'etut-proje/isTanimiListesi/$', EPProjectViews.return_employeetitles, name='istanimiListesi'),
    url(r'etut-proje/isTanimi/sil/(?P<pk>\d+)$', EPProjectViews.delete_employeetitle,
        name='unvan-sil'),
    # url(r'etut-proje/görev-duzenle/(?P<pk>\d+)$', EPProjectViews.edit_employeetitle,
    #     name='unvan-duzenle'),
    url(r'etut-proje/proje-personel-ekle/(?P<pk>\d+)$',
        EPProjectViews.add_employee_to_project, name='proje-personel-ekle'),
    url(r'etut-proje/personel/$', EPProjectViews.return_personel_dashboard, name='personel'),

    url(r'log/log-kayıtlari/$', LogViews.return_log,
        name='logs'),



    url(r'etut-proje/proje-personel-guncelle/(?P<pk>\d+)$',
        EPProjectViews.update_employee_to_project, name='proje-personel-guncelle'),
    url(r'etut-proje/proje-altproje-guncelle/(?P<pk>\d+)$',
        EPProjectViews.update_subcompany_to_project, name='proje-altproje-guncelle'),

    url(r'etut-proje/proje-altProjeFirma/(?P<pk>\d+)$',
        EPProjectViews.update_subcompany_information_to_project, name='proje-altproje-firmaBilgileri'),

    url(r'etut-proje/proje-altproje/(?P<pk>\d+)$',
        EPProjectViews.project_subfirma, name='proje-altfirma-ekle'),

    url(r'etut-proje/proje-hakedis-guncelle/(?P<pk>\d+)$',
        EPProjectViews.update_vest_to_project, name='proje-hakedis-guncelle'),



    url(r'etut-proje/proje-personel-sil/(?P<project_pk>\d+)/(?P<employee_pk>\d+)/$',
        EPProjectViews.delete_employee_from_project,
        name='proje-personel-kaldir'),

    url(r'etut-proje/proje-altfirma-sil/(?P<project_pk>\d+)/(?P<employee_pk>\d+)/$',
        EPProjectViews.delete_subcompany_project,
        name='proje-altfirma-kaldir'),
    url(r'etut-proje/proje-ihtiyac-ekle/(?P<pk>\d+)$',
        EPProjectViews.add_requirement_to_project, name='proje-ihtiyac-ekle'),
    url(r'etut-proje/proje-hakedis-ekle/(?P<pk>\d+)$',
        EPProjectViews.add_vest_to_project, name='proje-hakedis-ekle'),

    url(r'etut-proje/proje-ihtiyac-guncelle/(?P<pk>\d+)$',
        EPProjectViews.update_requirement_to_project, name='proje-ihtiyac-güncelle'),

    url(r'etut-proje/proje-ihtiyac-sil/(?P<project_pk>\d+)/(?P<employee_pk>\d+)/$',
        EPProjectViews.delete_requirement_from_project,
        name='proje-ihtiyac-kaldir'),
    url(r'etut-proje/proje-asama-ekle/(?P<pk>\d+)$',
        EPProjectViews.add_phase_to_project, name='proje-asama-ekle'),

    url(r'etut-proje/proje-asama-guncelle/(?P<pk>\d+)$',
        EPProjectViews.update_phase_to_project, name='proje-asama-guncelle'),



    url(r'etut-proje/proje-asama-sil/(?P<project_pk>\d+)/(?P<employee_pk>\d+)/$',
        EPProjectViews.delete_phase_from_project,
        name='proje-asama-kaldir'),
    url(r'etut-proje/proje-gorus-sil/(?P<project_pk>\d+)/(?P<employee_pk>\d+)/$',
        EPProjectViews.delete_ofters_from_project,
        name='proje-gorus-kaldir'),

    url(r'etut-proje/proje-hakedis-sil/(?P<project_pk>\d+)/(?P<employee_pk>\d+)/$',
        EPProjectViews.delete_vest_from_project,
        name='proje-hakedis-kaldir'),
    url(r'etut-proje/proje-oneri-ekle/(?P<pk>\d+)$',
        EPProjectViews.add_offer_to_project, name='proje-oneri-ekle'),
    # ajax ile personel ekleme
    url(r'etut-proje/proje-personel-bilgi/$',
        EPProjectViews.personel_list, name='personel-bilgi'),
    url(r'etut-proje/proje-ihtiyac-bilgi/$',
        EPProjectViews.ihtiyac_list, name='ihtiyac-bilgi'),
    url(r'etut-proje/proje-asama-bilgi/$',
        EPProjectViews.asama_list, name='asama-bilgi'),
    url(r'etut-proje/proje-town/$',
        EPProjectViews.town, name='ilce-bilgi'),
    url(r'etut-proje/proje/delete/(?P<pk>\d+)$', EPProjectViews.deleteReferee,
        name='proje-delete'),
    url(r'etut-proje/proje-dokuman-sil/(?P<project_pk>\d+)/(?P<employee_pk>\d+)/$',
        EPProjectViews.delete_document_project,
        name='proje-dokuman-kaldir'),

    url(r'etut-proje/proje-needdokuman-sil/(?P<project_pk>\d+)/(?P<employee_pk>\d+)/$',
        EPProjectViews.delete_needdocument_project,
        name='proje-ihtiyacDokuman-kaldir'),


    url(r'personel/personeller/$', EmployeeViews.return_employees, name='personeller'),
    url(r'personel/personeller/hepsi/$', EmployeeViews.return_employees_all, name='personeller-all'),
    url(r'personel/personel-ekle/$', EmployeeViews.add_employee, name='personel-ekle'),
    url(r'personel/personel-duzenle/(?P<pk>\d+)$', EmployeeViews.edit_employee, name='personel-duzenle'),
    url(r'personel/unvanListesi/$', EmployeeViews.return_workdefinitionslist, name='unvanlistesi'),
    url(r'personel/istanimi/sil/(?P<pk>\d+)$', EmployeeViews.delete_workdefinition,
        name='istanimi-sil'),
    url(r'personel/isTanimi-duzenle/(?P<pk>\d+)$', EmployeeViews.edit_workdefinition,
        name='istanimi-duzenle'),
    url(r'personel/Unvan-duzenle/(?P<pk>\d+)$', EmployeeViews.edit_workdefinitionUnvan,
        name='unvan-duzenle'),
    url(r'personel/personel-profil-guncelle/$', EmployeeViews.updateRefereeProfile,
        name='personel-profil-guncelle'),


#     pdf test

    url(r'pdf/$',PdfView.return_pdf, name='pdf'),
    url(r'pdf2/$', PdfView.html_to_pdf_view, name='pdf2'),
    url(r'pdf3/$', PdfView.return_pdf2, name='pdf3'),





    url(r'excel/$',PdfView.return_excel, name='excel'),
    url(r'excel2/$', PdfView.return_excel_row, name='excel2'),
    url(r'excel/personeller$', PdfView.return_excel_row_personel, name='excel-personel'),



     # technical
    url(r'etut-proje/teknik/$', TechnicalViews.return_technical_dashboard, name='anasayfa-teknik'),
    url(r'etut-proje/projeler/teknik$', TechnicalViews.return_projects, name='projeler-teknik'),
    url(r'etut-proje/proje-duzenle/teknik/(?P<pk>\d+)$', TechnicalViews.edit_project_personel,
        name='proje-incele-teknik'),
    url(r'etut-proje/personel-profil-guncelle/$', TechnicalViews.updateRefereeProfile,
        name='teknik-profil-guncelle'),
    url(r'teknik/personeller/$', TechnicalViews.return_employees, name='personeller-teknik'),
    url(r'teknik/personel-ekle/$', TechnicalViews.add_employee, name='personel-ekle-teknik'),

    url(r'notification/notification-all/$', NotificationView.notification, name='bildirimler'),

    url(r'message/$', DashboardViews.return_message,
        name='message'),

    path(r'message/api/v1/', include(router.urls)),

    # url(r'hello/$', TestList.as_view(), name='hello'),

    #     company
    url(r'company/company-add/$', CompanyView.return_add_Company, name='company-add'),
    url(r'company/company-list/$', CompanyView.return_list_Company, name='company-list'),
    url(r'company/company-update/(?P<pk>\d+)$', CompanyView.return_update_Company, name='company-update'),

    url(r'destek-talep-listesi', ClaimView.return_claim, name='destek-talep-listesi'),
    url(r'destek/Destekekle', ClaimView.claim_add, name='destek-talep-ekle'),
    url(r'destek/sil/(?P<pk>\d+)$', ClaimView.claim_delete, name='destek-delete'),
    url(r'destek/guncelle/(?P<pk>\d+)$', ClaimView.claim_update, name='destek-guncelle'),

    url(r'menu', ClaimView.menu, name='destek-talep-menu'),




]
