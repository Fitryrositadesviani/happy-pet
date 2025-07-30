# ... (kode di atasnya sama) ...

    elif page_selection == "Lihat Catatan Tersimpan":
        st.title("🍯 Catatan Anda") # <--- PERUBAHAN DI SINI
        notes = load_json_data(USER_NOTES_FILE)

        # Menampilkan pesan konfirmasi yang disimpan di session_state
        if 'user_notes_message' in st.session_state and st.session_state.user_notes_message:
            if st.session_state.user_notes_message_type == 'success':
                st.success(st.session_state.user_notes_message)
            elif st.session_state.user_notes_message_type == 'warning':
                st.warning(st.session_state.user_notes_message)
            elif st.session_state.user_notes_message_type == 'info':
                st.info(st.session_state.user_notes_message)
            st.session_state.user_notes_message = "" # Reset pesan setelah ditampilkan
            st.session_state.user_notes_message_type = ""

        if "user_notes" in notes and notes["user_notes"]:
            # --- Tampilkan Daftar Kategori sebagai Navigasi ---
            st.subheader("Daftar Kategori Anda:")
            col_idx = 0
            cols = st.columns(4)
            user_categories = list(notes["user_notes"].keys())
            
            if 'user_scroll_to_category' not in st.session_state:
                st.session_state.user_scroll_to_category = None

            for category_name in user_categories:
                with cols[col_idx]:
                    if st.button(category_name, key=f"user_nav_btn_{category_name}"):
                        st.session_state.user_selected_category_nav = category_name
                        st.session_state.user_scroll_to_category = category_name
                col_idx = (col_idx + 1) % 4
            
            st.markdown("---")

            # --- Tampilkan Catatan Berdasarkan Kategori ---
            target_category = st.session_state.get('user_selected_category_nav')

            if target_category and target_category in notes["user_notes"]:
                st.header(f"🌷 Kategori: {target_category}") # <--- PERUBAHAN DI SINI
                st.markdown(f"<a id='user_{target_category.replace(' ', '_')}'></a>", unsafe_allow_html=True)
                
                category_content = notes["user_notes"][target_category]
                if isinstance(category_content, dict):
                    display_section_content(category_content, level=1)
                elif isinstance(category_content, list):
                    for item in category_content:
                        st.markdown(f"- {item}")
                else:
                    st.markdown(f"- {category_content}")
                
                st.markdown("---")
                st.subheader("Kategori Anda Lainnya:")
                for category, content in notes["user_notes"].items():
                    if category != target_category:
                        st.header(f"🌷 Kategori: {category}") # <--- PERUBAHAN DI SINI
                        st.markdown(f"<a id='user_{category.replace(' ', '_')}'></a>", unsafe_allow_html=True)
                        if isinstance(content, dict):
                            display_section_content(content, level=1)
                        elif isinstance(content, list):
                            for item in content:
                                st.markdown(f"- {item}")
                        else:
                            st.markdown(f"- {content}")

# ... (kode di bawahnya sama) ...
