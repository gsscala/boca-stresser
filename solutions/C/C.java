import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class C {
    static class Point {
        long x, y;
        Point(long x, long y) {
            this.x = x;
            this.y = y;
        }
    }

    static final Point[] sao_paulo = {
        new Point(0, 100), new Point(100, 0), new Point(200, 0), new Point(100, -100),
        new Point(0, -100), new Point(-100, 0), new Point(-200, 0), new Point(-100, 100)
    };

    static long crossProduct(Point a, Point b, Point c) {
        return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
    }

    static boolean onSegment(Point p, Point a, Point b) {
        if (crossProduct(a, b, p) == 0) {
            if (p.x >= Math.min(a.x, b.x) && p.x <= Math.max(a.x, b.x) &&
                p.y >= Math.min(a.y, b.y) && p.y <= Math.max(a.y, b.y)) {
                return true;
            }
        }
        return false;
    }

    static boolean isInsideOrOnBorder(Point p) {
        int n = sao_paulo.length;
        boolean inside = false;
        for (int i = 0, j = n - 1; i < n; j = i++) {
            if (onSegment(p, sao_paulo[i], sao_paulo[j])) {
                return true;
            }
            if (((sao_paulo[i].y > p.y) != (sao_paulo[j].y > p.y))) {
                double intersectX = (double)(sao_paulo[j].x - sao_paulo[i].x) * (p.y - sao_paulo[i].y) / (double)(sao_paulo[j].y - sao_paulo[i].y) + sao_paulo[i].x;
                if (p.x < intersectX) {
                    inside = !inside;
                }
            }
        }
        return inside;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        int N = Integer.parseInt(line.trim());
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < N; i++) {
            line = br.readLine();
            if (line == null) break;
            StringTokenizer st = new StringTokenizer(line);
            long x = Long.parseLong(st.nextToken());
            long y = Long.parseLong(st.nextToken());
            if (isInsideOrOnBorder(new Point(x, y))) {
                sb.append("S\n");
            } else {
                sb.append("N\n");
            }
        }
        System.out.print(sb.toString());
    }
}
