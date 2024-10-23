from django.shortcuts import render, get_object_or_404, redirect
from .models import Sneaker

def view_keranjang(request):
    # Ambil keranjang dari sesi (buat keranjang kosong jika tidak ada)
    keranjang = request.session.get('keranjang', {})
    
    # Ambil semua item sneaker dalam keranjang dari database
    item_keranjang = []
    total_harga = 0
    for item_id, kuantitas in keranjang.items():
        sneaker = get_object_or_404(Sneaker, id=item_id)
        item_keranjang.append({
            'sneaker': sneaker,
            'kuantitas': kuantitas,
            'total_harga': sneaker.price * kuantitas,
        })
        total_harga += sneaker.price * kuantitas

    # Tambahkan flag item_added untuk menampilkan pesan sukses
    item_added = request.session.get('item_added', False)
    
    # Set item_added menjadi False setelah ditampilkan sekali
    request.session['item_added'] = False

    # Render halaman keranjang
    return render(request, 'keranjang.html', {
        'item_keranjang': item_keranjang,
        'total_harga': total_harga,
        'item_added': item_added,  # Tambahkan flag item_added ke konteks
    })

def add_to_cart(request, item_id):
    # Dapatkan produk Sneaker
    sneaker = get_object_or_404(Sneaker, id=item_id)
    
    # Ambil keranjang dari sesi (atau buat yang baru jika tidak ada)
    keranjang = request.session.get('keranjang', {})

    # Tambahkan item ke keranjang (atau tambah kuantitas jika sudah ada)
    if str(item_id) in keranjang:
        keranjang[str(item_id)] += 1
    else:
        keranjang[str(item_id)] = 1

    # Simpan keranjang yang diperbarui kembali ke sesi
    request.session['keranjang'] = keranjang

    # Set flag untuk menunjukkan item berhasil ditambahkan
    request.session['item_added'] = True
    
    return redirect('keranjang:view_keranjang')

def remove_from_cart(request, item_id):
    # Ambil keranjang dari sesi
    keranjang = request.session.get('keranjang', {})

    # Hapus item dari keranjang jika ada
    if str(item_id) in keranjang:
        del keranjang[str(item_id)]

    # Simpan keranjang yang diperbarui ke sesi
    request.session['keranjang'] = keranjang
    
    return redirect('keranjang:view_keranjang')

def checkout(request):
    return render(request, 'checkout.html') 