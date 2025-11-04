import pygame
import math


class Physics:

    def __init__(self, game):
        self.game = game

    @staticmethod
    def to_pygame(p):
        """Convert pymunk to pygame coordinates"""
        return (int(p.x), int(-p.y + 600))

    @staticmethod
    def vector(p0, p1):
        """Return the vector of the points
        p0 = (xo, yo), p1 = (x1, y1)"""
        a = p1[0] - p0[0]
        b = p1[1] - p0[1]
        return (a, b)

    @staticmethod
    def unit_vector(v):
        """Return the unit vector of the points
        v = (a, b)"""
        h = (v[0] ** 2 + v[1] ** 2) ** 0.5
        if h == 0:
            h = 1e-15
        ua = v[0] / h
        ub = v[1] / h
        return (ua, ub)

    @staticmethod
    def distance(xo, yo, x, y):
        """distance between points"""
        dx = x - xo
        dy = y - yo
        d = (dx ** 2 + dy ** 2) ** 0.5
        return d

    def post_solve_bird_pig(self, arbiter, space, _):
        """Collision between bird and pig"""
        surface = self.game.screen
        a, b = arbiter.shapes
        bird_body = a.body
        pig_body = b.body
        p = self.to_pygame(bird_body.position)
        p2 = self.to_pygame(pig_body.position)
        r = 30
        pygame.draw.circle(surface, self.game.BLACK, p, r, 4)
        pygame.draw.circle(surface, self.game.RED, p2, r, 4)
        pigs_to_remove = []
        for pig in self.game.pigs:
            if pig_body == pig.body:
                pig.life -= 20
                pigs_to_remove.append(pig)
                self.game.score += 10000
        for pig in pigs_to_remove:
            self.game.resources.play_pig_sound()
            self.game.space.remove(pig.shape, pig.shape.body)
            self.game.pigs.remove(pig)

    def post_solve_bird_wood(self, arbiter, space, _):
        """Collision between bird and wood"""
        poly_to_remove = []
        if arbiter.total_impulse.length > 1100:
            a, b = arbiter.shapes
            for column in self.game.columns:
                if b == column.shape:
                    poly_to_remove.append(column)
            for beam in self.game.beams:
                if b == beam.shape:
                    poly_to_remove.append(beam)
            for poly in poly_to_remove:
                if poly in self.game.columns:
                    self.game.columns.remove(poly)
                if poly in self.game.beams:
                    self.game.beams.remove(poly)
            self.game.space.remove(b, b.body)
            self.game.score += 5000

    def post_solve_pig_wood(self, arbiter, space, _):
        """Collision between pig and wood"""
        pigs_to_remove = []
        if arbiter.total_impulse.length > 700:
            pig_shape, wood_shape = arbiter.shapes
            for pig in self.game.pigs:
                if pig_shape == pig.shape:
                    pig.life -= 20
                    self.game.score += 10000
                    if pig.life <= 0:
                        pigs_to_remove.append(pig)
        for pig in pigs_to_remove:
            self.game.resources.play_pig_sound()
            self.game.space.remove(pig.shape, pig.shape.body)
            self.game.pigs.remove(pig)

    def setup_collision_handlers(self):
        """Setup collision handlers"""

        self.game.space.on_collision(0, 1, post_solve=self.post_solve_bird_pig)
        self.game.space.on_collision(0, 2, post_solve=self.post_solve_bird_wood)
        self.game.space.on_collision(1, 2, post_solve=self.post_solve_pig_wood)

    def sling_action(self):
        """Set up the sling behavior using computer vision"""
        v = self.vector((self.game.sling_x, self.game.sling_y), (self.game.x_mouse, self.game.y_mouse))
        uv = self.unit_vector(v)
        uv1, uv2 = (uv[0], uv[1])
        self.game.mouse_distance = self.distance(self.game.sling_x, self.game.sling_y, self.game.x_mouse, self.game.y_mouse)
        pu = (uv1 * self.game.rope_length + self.game.sling_x, uv2 * self.game.rope_length + self.game.sling_y)
        bigger_rope = 102
        x_redbird = self.game.x_mouse - 20
        y_redbird = self.game.y_mouse - 20
        if self.game.mouse_distance > self.game.rope_length:
            pux, puy = pu
            pux -= 20
            puy -= 20
            pul = (pux, puy)
            self.game.screen.blit(self.game.redbird, pul)
            pu2 = (uv1 * bigger_rope + self.game.sling_x, uv2 * bigger_rope + self.game.sling_y)
            pygame.draw.line(self.game.screen, (0, 0, 0), (self.game.sling2_x, self.game.sling2_y), pu2, 5)
            pygame.draw.line(self.game.screen, (0, 0, 0), (self.game.sling_x, self.game.sling_y), pu2, 5)
        else:
            self.game.mouse_distance += 10
            pu3 = (uv1 * self.game.mouse_distance + self.game.sling_x, uv2 * self.game.mouse_distance + self.game.sling_y)
            pygame.draw.line(self.game.screen, (0, 0, 0), (self.game.sling2_x, self.game.sling2_y), pu3, 5)
            self.game.screen.blit(self.game.redbird, (x_redbird, y_redbird))
            pygame.draw.line(self.game.screen, (0, 0, 0), (self.game.sling_x, self.game.sling_y), pu3, 5)
        dy = self.game.y_mouse - self.game.sling_y
        dx = self.game.x_mouse - self.game.sling_x
        if dx == 0:
            dx = 1e-14
        self.game.angle = math.atan(float(dy) / dx)

    def update_physics(self):
        dt = 0.01
        for _ in range(2):
            self.game.space.step(dt)
