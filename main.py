from shape import *


def main():
    def destroy_canvas(event):
        print(f"you've hit {a.shapes_hit} out of {a.shape_counter} shapes "
              f"and missclicked {a.shapes_miss} times ")
        root.destroy()

    a = Storage()
    a.tick()
    canv.bind('<Button-2>', destroy_canvas)
    tk.mainloop()
    # print(f"you've hit {hit} times and missed {miss}")


if __name__ == "__main__":
    main()








