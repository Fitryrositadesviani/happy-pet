import streamlit as st
import json
import os

# Nama file untuk menyimpan catatan yang ditambahkan/diedit pengguna
USER_NOTES_FILE = 'user_notes.json'
# Nama file untuk menyimpan catatan default (yang bisa diedit admin)
DEFAULT_NOTES_FILE = 'default_notes.json'

def load_json_data(file_path):
    """Memuat data dari file JSON."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            st.error(f"Error: Gagal membaca file JSON '{file_path}'. Pastikan formatnya benar.")
            return {}
    return {}

def save_json_data(data, file_path):
    """Menyimpan data ke file JSON."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def display_section(title, items):
    """Fungsi pembantu untuk menampilkan bagian dengan bullet points."""
    st.subheader(title)
    if isinstance(items, list):
        for item in items:
            st.markdown(f"- {item}")
    elif isinstance(items, dict):
        for key, value in items.items():
            if isinstance(value, list):
                st.markdown(f"- **{key}**:")
                for sub_item in value:
                    st.markdown(f"  - {sub_item}")
            else:
                st.markdown(f"- **{key}**: {value}")
    else:
        st.write(items) # Untuk kasus single line

def display_notes_data(notes_data_to_display):
    """Menampilkan data catatan yang sudah ada dalam format rapi."""
    st.title("🗒️ Catatan Happy Pet & Pengetahuan Umum")

    # Menampilkan setiap bagian
    for category, content in notes_data_to_display.items():
        st.header(f"✨ {category}")
        if isinstance(content, dict):
            for sub_category, items in content.items():
                display_section(f"**{sub_category}**", items)
        elif isinstance(content, list):
            for item in content:
                st.markdown(f"- {item}")
        else:
            st.write(content)


def main():
    st.set_page_config(layout="wide")

    st.sidebar.title("Navigasi")
    page_selection = st.sidebar.radio("Pilih Halaman", ["Lihat Catatan Tersimpan", "Tambah Catatan Baru", "Catatan Default Happy Pet", "Edit Catatan Default"])

    if page_selection == "Catatan Default Happy Pet":
        default_notes = load_json_data(DEFAULT_NOTES_FILE)
        if default_notes:
            display_notes_data(default_notes)
        else:
            st.info("Tidak ada catatan default yang ditemukan atau ada kesalahan saat memuat.")

    elif page_selection == "Tambah Catatan Baru":
        st.title("➕ Tambah Catatan Baru")
        note_title = st.text_input("Judul Catatan")
        note_content = st.text_area("Isi Catatan Anda", height=200)

        if st.button("Simpan Catatan"):
            if note_title and note_content:
                notes = load_json_data(USER_NOTES_FILE)
                if "user_notes" not in notes:
                    notes["user_notes"] = {}
                notes["user_notes"][note_title] = note_content
                save_json_data(notes, USER_NOTES_FILE)
                st.success("Catatan berhasil disimpan!")
                st.write(f"**Judul:** {note_title}")
                st.write(f"**Isi:** {note_content}")
            else:
                st.warning("Judul dan isi catatan tidak boleh kosong.")

    elif page_selection == "Lihat Catatan Tersimpan":
        st.title("📚 Catatan Anda")
        notes = load_json_data(USER_NOTES_FILE)

        if "user_notes" in notes and notes["user_notes"]:
            st.write("Berikut adalah catatan yang Anda simpan:")
            # Tampilan catatan dengan opsi hapus
            for title, content in notes["user_notes"].items():
                col1, col2 = st.columns([0.7, 0.3])
                with col1:
                    st.subheader(title)
                    st.write(content)
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True) # Jarak agar tombol tidak terlalu dekat
                    if st.button(f"Hapus '{title}'", key=f"delete_{title}"):
                        del notes["user_notes"][title]
                        save_json_data(notes, USER_NOTES_FILE)
                        st.experimental_rerun() # Refresh halaman setelah menghapus

            # Bagian untuk mengedit catatan
            st.markdown("---")
            st.subheader("Edit Catatan (Pilih salah satu)")
            selected_note_to_edit = st.selectbox(
                "Pilih catatan untuk diedit:",
                [""] + list(notes["user_notes"].keys()),
                key="select_user_note_to_edit"
            )

            if selected_note_to_edit:
                if 'edited_user_title' not in st.session_state or st.session_state.edited_user_title != selected_note_to_edit:
                    st.session_state.edited_user_title = selected_note_to_edit
                    st.session_state.edited_user_content = notes["user_notes"][selected_note_to_edit]

                new_title = st.text_input("Judul Baru:", value=st.session_state.edited_user_title, key="edit_user_title_input")
                new_content = st.text_area("Isi Baru:", value=st.session_state.edited_user_content, height=200, key="edit_user_content_area")

                if st.button("Update Catatan", key="update_user_note_button"):
                    if new_title and new_content:
                        if new_title != st.session_state.edited_user_title:
                            del notes["user_notes"][st.session_state.edited_user_title]
                        notes["user_notes"][new_title] = new_content
                        save_json_data(notes, USER_NOTES_FILE)
                        st.success("Catatan berhasil diperbarui!")
                        if 'edited_user_title' in st.session_state:
                            del st.session_state.edited_user_title
                        if 'edited_user_content' in st.session_state:
                            del st.session_state.edited_user_content
                        st.experimental_rerun()
                    else:
                        st.warning("Judul dan isi catatan tidak boleh kosong.")
        else:
            st.info("Anda belum memiliki catatan yang disimpan.")

    elif page_selection == "Edit Catatan Default":
        st.title("⚙️ Edit Catatan Default Happy Pet")
        st.warning("Halaman ini ditujukan untuk mengedit catatan default. Perubahan di sini akan mempengaruhi semua pengguna.")

        default_notes = load_json_data(DEFAULT_NOTES_FILE)

        if not default_notes:
            st.error("Tidak dapat memuat catatan default untuk diedit. Pastikan file 'default_notes.json' ada dan formatnya benar.")
            return

        # Tampilkan kategori dan sub-kategori untuk diedit
        st.subheader("Pilih Kategori untuk Diedit:")
        categories = list(default_notes.keys())
        selected_category = st.selectbox("Pilih Kategori:", [""] + categories, key="edit_default_category_select")

        if selected_category:
            category_content = default_notes[selected_category]

            # Jika konten kategori adalah dictionary (ada sub-kategori)
            if isinstance(category_content, dict):
                st.subheader(f"Konten Kategori: {selected_category}")
                sub_categories = list(category_content.keys())
                selected_sub_category = st.selectbox(
                    "Pilih Sub-Kategori:",
                    [""] + sub_categories,
                    key="edit_default_sub_category_select"
                )

                if selected_sub_category:
                    item_content = category_content[selected_sub_category]

                    st.markdown(f"**Mengedit: {selected_category} > {selected_sub_category}**")

                    # Jika konten adalah list (daftar item)
                    if isinstance(item_content, list):
                        edited_list_str = st.text_area(
                            "Edit daftar item (satu item per baris):",
                            value="\n".join(item_content),
                            height=250,
                            key="edit_default_list_area"
                        )
                        updated_items = [item.strip() for item in edited_list_str.split('\n') if item.strip()]
                        if st.button("Simpan Perubahan Sub-Kategori"):
                            default_notes[selected_category][selected_sub_category] = updated_items
                            save_json_data(default_notes, DEFAULT_NOTES_FILE)
                            st.success("Catatan default berhasil diperbarui!")
                            st.experimental_rerun()

                    # Jika konten adalah string (nilai tunggal)
                    elif isinstance(item_content, str):
                        edited_str_value = st.text_input(
                            "Edit nilai:",
                            value=item_content,
                            key="edit_default_string_input"
                        )
                        if st.button("Simpan Perubahan Sub-Kategori"):
                            default_notes[selected_category][selected_sub_category] = edited_str_value
                            save_json_data(default_notes, DEFAULT_NOTES_FILE)
                            st.success("Catatan default berhasil diperbarui!")
                            st.experimental_rerun()
                    else:
                        st.info("Tipe data tidak didukung untuk pengeditan langsung di sini (bukan daftar atau teks).")

            # Jika konten kategori adalah list (daftar item langsung di bawah kategori)
            elif isinstance(category_content, list):
                st.subheader(f"Konten Kategori: {selected_category}")
                edited_list_str = st.text_area(
                    "Edit daftar item (satu item per baris):",
                    value="\n".join(category_content),
                    height=250,
                    key="edit_default_category_list_area"
                )
                updated_items = [item.strip() for item in edited_list_str.split('\n') if item.strip()]
                if st.button("Simpan Perubahan Kategori"):
                    default_notes[selected_category] = updated_items
                    save_json_data(default_notes, DEFAULT_NOTES_FILE)
                    st.success("Catatan default berhasil diperbarui!")
                    st.experimental_rerun()

            # Jika konten kategori adalah string (nilai tunggal langsung di bawah kategori)
            elif isinstance(category_content, str):
                st.subheader(f"Konten Kategori: {selected_category}")
                edited_str_value = st.text_input(
                    "Edit nilai:",
                    value=category_content,
                    key="edit_default_category_string_input"
                )
                if st.button("Simpan Perubahan Kategori"):
                    default_notes[selected_category] = edited_str_value
                    save_json_data(default_notes, DEFAULT_NOTES_FILE)
                    st.success("Catatan default berhasil diperbarui!")
                    st.experimental_rerun()
            else:
                st.info("Tipe data tidak didukung untuk pengeditan langsung di sini (bukan daftar, teks, atau kamus).")

        st.markdown("---")
        st.subheader("Tambahkan Kategori Baru ke Catatan Default")
        new_category_name = st.text_input("Nama Kategori Baru:", key="new_default_category_name")
        new_category_type = st.radio("Tipe Konten Kategori Baru:", ["Daftar (item per baris)", "Teks Tunggal"], key="new_default_category_type")
        new_category_content = st.text_area("Isi Kategori Baru (pisahkan dengan baris baru jika daftar):", height=150, key="new_default_category_content")

        if st.button("Tambah Kategori Baru", key="add_new_default_category_button"):
            if new_category_name and new_category_content:
                if new_category_type == "Daftar (item per baris)":
                    items = [item.strip() for item in new_category_content.split('\n') if item.strip()]
                    default_notes[new_category_name] = items
                else:
                    default_notes[new_category_name] = new_category_content.strip()
                save_json_data(default_notes, DEFAULT_NOTES_FILE)
                st.success(f"Kategori '{new_category_name}' berhasil ditambahkan!")
                st.experimental_rerun()
            else:
                st.warning("Nama kategori dan isi tidak boleh kosong.")

        st.markdown("---")
        st.subheader("Hapus Kategori dari Catatan Default")
        category_to_delete = st.selectbox("Pilih Kategori yang akan dihapus:", [""] + categories, key="delete_default_category_select")
        if category_to_delete and st.button(f"Hapus Kategori '{category_to_delete}'", key="delete_default_category_button"):
            confirm = st.checkbox(f"Saya yakin ingin menghapus kategori '{category_to_delete}'", key="confirm_delete_default_category")
            if confirm:
                del default_notes[category_to_delete]
                save_json_data(default_notes, DEFAULT_NOTES_FILE)
                st.success(f"Kategori '{category_to_delete}' berhasil dihapus.")
                st.experimental_rerun()
            else:
                st.info("Centang kotak konfirmasi untuk menghapus.")


if __name__ == "__main__":
    main()
