import cv2
import numpy as np
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import imutils

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# Konfigurasi Standarisasi & Satuan
LEBAR_REFERENSI_CM = 8.5 
TARGET_PIXEL_SIM = 220  
TOLERANSI = 30          
opsi_satuan = [("cm", 1.0), ("mm", 10.0), ("inch", 0.393701)]
indeks_satuan = 0

# Mengakses kamera utama
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("GAGAL: Kamera tidak dapat diakses.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal menangkap gambar dari kamera.")
        break
        
    frame = imutils.resize(frame, width=800)
    orig = frame.copy()
    
    H, W = orig.shape[:2]
    nama_satuan, pengali = opsi_satuan[indeks_satuan]
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:2]
        
        if len(cnts) == 2:
            (cnts, _) = contours.sort_contours(cnts)
            pixelsPerMetric = None

            for c in cnts:
                if cv2.contourArea(c) < 2000: 
                    continue

                box = cv2.minAreaRect(c)
                box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
                box = np.array(box, dtype="int")
                box = perspective.order_points(box)
                
                cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

                (tl, tr, br, bl) = box
                (tltrX, tltrY) = midpoint(tl, tr)
                (blbrX, blbrY) = midpoint(bl, br)
                (tlblX, tlblY) = midpoint(tl, bl)
                (trbrX, trbrY) = midpoint(tr, br)

                dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
                dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                sisi_terpanjang = max(dA, dB)

                if pixelsPerMetric is None:
                    # Logika Standarisasi Jarak berbasis objek paling kiri (Referensi)
                    pixelsPerMetric = sisi_terpanjang / LEBAR_REFERENSI_CM
                    
                    if sisi_terpanjang < (TARGET_PIXEL_SIM - TOLERANSI):
                        cv2.putText(orig, "TERLALU JAUH - Dekatkan Kamera!", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    elif sisi_terpanjang > (TARGET_PIXEL_SIM + TOLERANSI):
                        cv2.putText(orig, "TERLALU DEKAT - Jauhkan Kamera!", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    else:
                        cv2.putText(orig, "JARAK KAMERA PAS", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                dimensiA = (dA / pixelsPerMetric) * pengali
                dimensiB = (dB / pixelsPerMetric) * pengali

                cv2.putText(orig, f"{dimensiB:.1f}{nama_satuan}", (int(tltrX - 15), int(tltrY - 10)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
                cv2.putText(orig, f"{dimensiA:.1f}{nama_satuan}", (int(trbrX + 10), int(trbrY)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

    cv2.putText(orig, f"Satuan: {nama_satuan.upper()} (Tekan 'u' ubah, 'q' keluar)", (20, H - 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.imshow("Hasil Pengukuran Live", orig)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('u'):
        indeks_satuan = (indeks_satuan + 1) % len(opsi_satuan)

cap.release()
cv2.destroyAllWindows()