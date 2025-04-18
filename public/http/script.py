from .main import MainController
from .print import (
    print_response,
    print_error,
    print_success,
    print_request,
    print_user_info
)

def main():
    # API yapılandırması
    BASE_URL = "https://api.example.com"
    API_KEY = "your-api-key"
    SECRET_KEY = "your-secret-key"
    
    # Controller oluştur
    controller = MainController(
        base_url=BASE_URL,
        api_key=API_KEY,
        secret_key=SECRET_KEY
    )
    
    try:
        # Kullanıcı kaydı
        user_data = {
            "username": "test_user",
            "password": "test_password",
            "email": "test@example.com"
        }
        
        print_request("POST", f"{BASE_URL}/users", data=user_data)
        register_result = controller.register(user_data)
        
        if register_result:
            print_success("Kullanıcı başarıyla kaydedildi")
            print_user_info(register_result["user"])
        else:
            print_error("Kullanıcı kaydı başarısız oldu")
            
        # Kullanıcı girişi
        print_request(
            "POST",
            f"{BASE_URL}/auth/login",
            data={"username": "test_user", "password": "test_password"}
        )
        login_result = controller.login("test_user", "test_password")
        
        if login_result:
            print_success("Kullanıcı başarıyla giriş yaptı")
            token = login_result["token"]
            
            # Kullanıcı bilgilerini getir
            print_request("GET", f"{BASE_URL}/users/test_user")
            user_info = controller.get_user_info("test_user")
            
            if user_info:
                print_success("Kullanıcı bilgileri alındı")
                print_user_info(user_info)
            else:
                print_error("Kullanıcı bilgileri alınamadı")
                
            # Kullanıcı bilgilerini güncelle
            update_data = {
                "email": "updated@example.com",
                "name": "Test User"
            }
            
            print_request(
                "PUT",
                f"{BASE_URL}/users/test_user",
                data=update_data
            )
            update_result = controller.update_user_info("test_user", update_data)
            
            if update_result:
                print_success("Kullanıcı bilgileri güncellendi")
                print_user_info(update_result)
            else:
                print_error("Kullanıcı bilgileri güncellenemedi")
                
            # Token'ı yenile
            print_request("POST", f"{BASE_URL}/auth/refresh")
            new_token = controller.refresh_token(token)
            
            if new_token:
                print_success("Token başarıyla yenilendi")
            else:
                print_error("Token yenilenemedi")
                
            # Çıkış yap
            print_request("POST", f"{BASE_URL}/auth/logout")
            if controller.logout(token):
                print_success("Kullanıcı başarıyla çıkış yaptı")
            else:
                print_error("Çıkış yapılamadı")
                
        else:
            print_error("Giriş başarısız oldu")
            
    except Exception as e:
        print_error("Bir hata oluştu", {"error": str(e)})
        
if __name__ == "__main__":
    main()
