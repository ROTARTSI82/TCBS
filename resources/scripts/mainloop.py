#!venv/bin python
# -*- coding: UTF-8 -*-

"""
(.../TCBS/resources/scripts/mainloop.py)
------------------------------------------------------------------------
TOTALLY CUSTOMIZABLE BATTLE SIMULATOR i21.18.03.31
------------------------------------------------------------------------
By Grant Yang

Totally Customizable Battle Simulator is a multiplayer
strategy videogame. You can design and program your
own soldiers and make them fight against your
friend's soldiers. It is inspired by Totally Accurate
Battle Simulator by Landfall and uses Pygame 1.9 and
Python 2.7. TCBS uses PodSixNet written by chr15m (Chris McCormick).

SEE README.md FOR MORE DETAILS
"""
import webbrowser

if False:
    # Ignore this code. It makes PyCharm happy
    # Since I call this script via execfile, PyCharm thinks
    # all the variables are undefined and gives me endless warnings :(
    from load import *
    from CONFIG import *

__appName__ = "Totally Customizable Battle Simulator"
__version__ = "a21.18.04.14"
__author__ = "Grant Yang"

updaterects()
while running:
    clock.tick()
    cbCollide = pygame.sprite.spritecollide(cursor, buttons, False)
    for button in buttons:
        if button in cbCollide:
            button.updatehover(True)
        else:
            button.updatehover(False)
    screen.fill([red, green, blue])
    if __debugMode__:
        DebugFPSText = simpleFont.render("FPS: "+str(clock.get_fps()),
                                         False, [0, 0, 0], [255, 255, 255])
        screen.blit(DebugFPSText, [10, 10])
        screen.blit(cursor.image, cursor.rect)

    if state == "menu":
        if badVerDetect:
            screen.blit(badVerWarn.image, badVerWarn.rect)
        if newUpDetect:
            screen.blit(newUpNote.image, newUpNote.rect)
        screen.blit(playBt.image, playBt.rect)
        screen.blit(mltPlayBt.image, mltPlayBt.rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if mltPlayBt in cbCollide and event.button == 1 and psnSuccess:
                    menuBlip.play()
                    state = "mult-start"
                if newUpNote in cbCollide and event.button == 1 and newUpDetect:
                    menuBlip.play()
                    try:
                        webbrowser.open("https://sites.google.com/site/rotartsiofficial/python-games/tcbs")
                    except Exception as e:
                        if not str(e) in alreadyHandled:
                            log("EXCEPTION", "Cannot open link: "+str(e))
                            alreadyHandled.append(str(e))
                if badVerWarn in cbCollide and event.button == 1 and badVerDetect:
                    menuBlip.play()
                    try:
                        webbrowser.open("https://sites.google.com/site/rotartsiofficial/help/badver")
                    except Exception as e:
                        if not str(e) in alreadyHandled:
                            log("EXCEPTION", "Cannot open link: "+str(e))
                            alreadyHandled.append(str(e))
                if playBt in cbCollide and event.button == 1:
                    menuBlip.play()
                    state = "sndbx-placeUnits"
                    updateselectedunit(0)
                    set_music("resources/sounds/in-gameMusic.wav")
            if event.type == KEYDOWN:
                if event.key == screenshotKey:
                    take_screenshot()
            if event.type == MOUSEMOTION:
                cursor.rect.center = event.pos
            if event.type == QUIT:
                running = False
            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict['size'], *screenArgs[1:])
                updaterects()
    if state == "sndbx-placeUnits":
        pygame.draw.line(screen, [0, 200, 0], [screen.get_width() / 2, -5],
                         [screen.get_width() / 2, screen.get_height() + 5], 5)
        sndbxRUnits.draw(screen)
        sndbxBUnits.draw(screen)
        screen.blit(startBt.image, startBt.rect)
        screen.blit(backBt.image, backBt.rect)
        screen.blit(selectedUnitTxt.image, selectedUnitTxt.rect)
        screen.blit(nextBt.image, nextBt.rect)
        screen.blit(prevBt.image, prevBt.rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                sndbxCol = pygame.sprite.spritecollide(cursor, sndbxBts, False)
                if event.button == 1 and not sndbxCol:
                    try:
                        if cursor.rect.center[0] > screen.get_width()/2:
                            sndbxRUnits.add(unitList[selectedUnitInt][0](cursor.rect.center, "red"))
                        if cursor.rect.center[0] < screen.get_width()/2:
                            sndbxBUnits.add(unitList[selectedUnitInt][0](cursor.rect.center, "blue"))
                    except Exception as e:
                        if not str(e) in alreadyHandled:
                            log("EXCEPTION", "Cannot create unit instance: "+str(e))
                            alreadyHandled.append(str(e))
                if event.button == 3 and not sndbxCol:
                    pygame.sprite.spritecollide(cursor, sndbxBUnits, True)
                    pygame.sprite.spritecollide(cursor, sndbxRUnits, True)
                if startBt in cbCollide and event.button == 1:
                    state = "sndbx-battle"
                if backBt in cbCollide and event.button == 1:
                    menuBlip.play()
                    state = "menu"
                    set_music("resources/sounds/menuMusic.wav")
                if nextBt in cbCollide and event.button == 1:
                    menuBlip.play()
                    updateselectedunit(+1)
                if prevBt in cbCollide and event.button == 1:
                    menuBlip.play()
                    updateselectedunit(-1)
            if event.type == KEYDOWN:
                if event.key == screenshotKey:
                    take_screenshot()
            if event.type == QUIT:
                running = False
            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict['size'], *screenArgs[1:])
                updaterects()
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.center = event.pos
    if state == "sndbx-battle":
        if len(sndbxRUnits) == 0 and len(sndbxBUnits) == 0:
            log("BATTLEOVER", "Draw!")
            state = "sndbx-placeUnits"
        if len(sndbxRUnits) == 0:
            log("BATTLEOVER", "Blue Victory!")
            state = "sndbx-placeUnits"
        if len(sndbxBUnits) == 0:
            log("BATTLEOVER", "Red Victory!")
            state = "sndbx-placeUnits"
        BbulletCol = pygame.sprite.groupcollide(bullets, sndbxBUnits, False, False)
        RbulletCol = pygame.sprite.groupcollide(bullets, sndbxBUnits, False, False)
        soldierCol = pygame.sprite.groupcollide(sndbxBUnits, sndbxRUnits, False, False)
        sndbxRUnits.update()
        sndbxBUnits.update()
        bullets.update()
        for i in BbulletCol.keys():
            i.onBulletHit(BbulletCol[i])
            for j in BbulletCol[i]:
                j.onBulletHit([i, ])
        for i in RbulletCol.keys():
            i.onBulletHit(RbulletCol[i])
            for j in RbulletCol[i]:
                j.onBulletHit([i, ])
        for i in soldierCol.keys():
            i.onSoldierHit(soldierCol[i])
            for j in soldierCol[i]:
                j.onSoldierHit([i, ])
        sndbxRUnits.draw(screen)
        sndbxBUnits.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEMOTION:
                cursor.rect.center = event.pos
            if event.type == KEYDOWN:
                if event.key == screenshotKey:
                    take_screenshot()
                if event.key == endBattleKey:
                    state = "sndbx-placeUnits"
    if state == "mult-start":
        screen.blit(backBt.image, backBt.rect)
        screen.blit(joinBt.image, joinBt.rect)
        screen.blit(serverMsg.image, serverMsg.rect)
        screen.blit(createBt.image, createBt.rect)
        screen.blit(coinRegenBt.image, coinRegenBt.rect)
        screen.blit(startBudgetBt.image, startBudgetBt.rect)
        screen.blit(serverHelpBt.image, serverHelpBt.rect)
        screen.blit(serverTxt.image, serverTxt.rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == copyKey:
                    pygame.scrap.put(SCRAP_TEXT, serverStr)
                    serverMsg = TxtOrBt(["Text Copied to Clipboard", False, [0, 0, 0]], [None, 45])
                    serverMsg.rect.center = [screen.get_width()/2, screen.get_height()/2-45]
                    continue
                if event.key == pasteKey:
                    serverStr = pygame.scrap.get(SCRAP_TEXT)
                    serverTxt = TxtOrBt([serverStr, False, [0, 0, 0]], [None, 45])
                    serverTxt.rect.center = [screen.get_width() / 2,
                                             screen.get_height() / 2]
                    continue
                if event.key == screenshotKey:
                    take_screenshot()
                if event.key == K_SPACE:
                    menuBlip.play()
                    serverStr += " "
                if pygame.key.name(event.key) in validChars:
                    menuBlip.play()
                    if not shiftDown:
                        serverStr = serverStr + pygame.key.name(event.key)
                    if shiftDown:
                        serverStr = serverStr + shiftChars[
                            validChars.find(pygame.key.name(event.key))]
                if event.key == K_LSHIFT or event.key == K_RSHIFT:
                    shiftDown = True
                if event.key == K_BACKSPACE:
                    menuBlip.play()
                    try:
                        serverStr = serverStr[:-1]
                    except Exception as e:
                        serverStr = ""
                serverTxt = TxtOrBt([serverStr, False, [0, 0, 0]], [None, 45])
                serverTxt.rect.center = [screen.get_width()/2,
                                         screen.get_height()/2]
            if event.type == KEYUP:
                if event.key == K_LSHIFT or event.key == K_RSHIFT:
                    shiftDown = False
            if event.type == MOUSEBUTTONDOWN:
                if startBudgetBt in cbCollide:
                    if event.button == 1:
                        menuBlip.play()
                        startBdgt += 100
                        updateoptions()
                    if event.button == 3:
                        menuBlip.play()
                        startBdgt -= 100
                        updateoptions()
                if coinRegenBt in cbCollide:
                    if event.button == 1:
                        menuBlip.play()
                        coinRR += 100
                        updateoptions()
                    if event.button == 3:
                        menuBlip.play()
                        coinRR -= 100
                        updateoptions()
                if joinBt in cbCollide and event.button == 1:
                    menuBlip.play()
                    try:
                        args = serverStr.split(":")
                        selfIsHost = False
                        c = TCBSClient(args[0], int(args[1]))
                        state = "mult-wait4players"
                        set_music("resources/sounds/in-gameMusic.wav")
                    except Exception as e:
                        if not str(e) in alreadyHandled:
                            log("EXCEPTION", "Cannot join game: "+str(e))
                            alreadyHandled.append(str(e))
                        serverMsg = TxtOrBt([str(e), False, [255, 0, 0]], [None, 45])
                        serverMsg.rect.center = [screen.get_width()/2,
                                                 screen.get_height()/2-45]
                if createBt in cbCollide and event.button == 1:
                    menuBlip.play()
                    try:
                        args = serverStr.split(":")
                        selfIsHost = True
                        s = TCBSServer(localaddr=(args[0], int(args[1])))
                        c = TCBSClient(args[0], int(args[1]))
                        state = "mult-wait4players"
                        set_music("resources/sounds/in-gameMusic.wav")
                    except Exception as e:
                        if not str(e) in alreadyHandled:
                            log("EXCEPTION", "Cannot create game: "+str(e))
                            alreadyHandled.append(str(e))
                        serverMsg = TxtOrBt([str(e), False, [255, 0, 0]], [None, 45])
                        serverMsg.rect.center = [screen.get_width()/2,
                                                 screen.get_height()/2-45]
                if serverHelpBt in cbCollide and event.button == 1:
                    menuBlip.play()
                    try:
                        webbrowser.open("https://sites.google.com/site/rotartsiofficial/help/server")
                    except Exception as e:
                        if not str(e) in alreadyHandled:
                            log("EXCEPTION", "Cannot open link: "+str(e))
                            alreadyHandled.append(str(e))
                if backBt in cbCollide and event.button == 1:
                    menuBlip.play()
                    state = "menu"
            if event.type == QUIT:
                running = False
            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict['size'], *screenArgs[1:])
                updaterects()
            if event.type == MOUSEMOTION:
                cursor.rect.center = event.pos
    if state == "mult-wait4players":
        try:
            c.loop()
            if selfIsHost:
                s.loop()
        except Exception as e:
            log("EXCEPTION", "Cannot Pump: "+str(e))
            serverMsg = TxtOrBt([str(e), False, [255, 0, 0]], [None, 45])
            serverMsg.rect.center = [screen.get_width()/2,
                                     screen.get_height()/2-45]
            
            if selfIsHost:
                s.shutdown()
            state = "mult-start"
            set_music("resources/sounds/menuMusic.wav")
        screen.blit(backBt.image, backBt.rect)
        screen.blit(wait4plyrsTxt.image, wait4plyrsTxt.rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if backBt in cbCollide and event.button == 1:
                    menuBlip.play()
                    state = "mult-start"
                    if selfIsHost:
                        s.shutdown()
                    set_music("resources/sounds/menuMusic.wav")
            if event.type == KEYDOWN:
                if event.key == screenshotKey:
                    take_screenshot()
            if event.type == QUIT:
                if selfIsHost:
                    s.shutdown()
                running = False
            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict['size'], *screenArgs[1:])
                updaterects()
            if event.type == MOUSEMOTION:
                cursor.rect.center = event.pos
    if state == "mult-placeUnits":
        try:
            c.loop()
            if selfIsHost:
                s.loop()
        except Exception as e:
            log("EXCEPTION", "Cannot Pump: "+str(e))
            serverMsg = TxtOrBt([str(e), False, [255, 0, 0]], [None, 45])
            serverMsg.rect.center = [screen.get_width()/2,
                                     screen.get_height()/2-45]
            
            if selfIsHost:
                s.shutdown()
            state = "mult-start"
            set_music("resources/sounds/menuMusic.wav")
        screen.blit(backBt.image, backBt.rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                c.Send({"action": "test", "test": "Hello World!"})  # EXPIREMENTAL
                if backBt in cbCollide and event.button:
                    menuBlip.play()
                    state = "mult-start"
                    if selfIsHost:
                        s.shutdown()
                    set_music("resources/sounds/menuMusic.wav")
            if event.type == KEYDOWN:
                if event.key == screenshotKey:
                    take_screenshot()
            if event.type == QUIT:
                if selfIsHost:
                    s.shutdown()
                running = False
            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict['size'], *screenArgs[1:])
                updaterects()
            if event.type == MOUSEMOTION:
                cursor.rect.center = event.pos
pygame.quit()
try:
    connection.Close()
except Exception as e:
    log("EXCEPTION", "Cannot close connection: "+str(e))
end = datetime.datetime.now()
log("PERFORMANCE", "FPS: "+str(clock.get_fps()))
log("STOP", "Stopping...")
log("RUNTIME", "Session lasted "+str(end-start))